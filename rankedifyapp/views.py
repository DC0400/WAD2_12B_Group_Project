import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from rankedify import settings

import rankedifyapp
from .forms import ProfileForm, UserProfileForm
from .models import Profile, ListeningMinutesPerTime, Friends
from django.shortcuts import redirect
from django.urls import reverse

import time
import requests


def index(request):
    leaderboard = Profile.objects.order_by("-listening_minutes")[:12]
    return render(request, "rankedify/index.html", {"leaderboard": leaderboard})
@csrf_exempt
def receive_tracks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            #print("Received Top Tracks:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def receive_minutes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            #print("Received Minutes:", data)

            username = get_user_profile(request)
            for profiles in Profile.objects.all():
                if profiles.username == username:
                    #print(profiles.username)
                    profiles.listening_minutes += data
                    profiles.last_logged_in = (time.time()*1000)
                    profiles.save()

                    new_listening_time = ListeningMinutesPerTime.objects.create(username_minutes=profiles.profile, listening_minutes=profiles.listening_minutes, last_logged_in=profiles.last_logged_in)
                    new_listening_time.save()

            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def receive_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Profile:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def receive_photo(request):
    if request.method == "POST":
        try:
            photo_url = json.loads(request.body)

            #media_images_path = os.path.join(settings.MEDIA_DIR, "images")
            os.makedirs(settings.MEDIA_DIR, exist_ok=True)
            image_path = os.path.join(settings.MEDIA_DIR, get_user_profile(request) + ".jpg")

            response = requests.get(photo_url)
            if response.status_code == 200:
                with open(image_path, "wb") as file:
                    file.write(response.content)

                username = get_user_profile(request)
                for profiles in Profile.objects.all():
                    if profiles.username == username:
                        #print(profiles.username)
                        profiles.photo = image_path
                        profiles.save()

                #print("Photo received successfully")
            else:
                print("Photo not received")

            #print("Received Photo:", photo_url)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def receive_spotify_username(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = get_user_profile(request)
            for profiles in Profile.objects.all():
                if profiles.username == username:
                    #print(data)
                    profiles.spotify_username = data
                    profiles.save()

            #print("Received Profile:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def profile(request):
    context_dict = {}

    username = get_user_profile(request)
    for profiles in Profile.objects.all():
        if profiles.username == username:
            context_dict["top_song"] = profiles.top_song
            context_dict["spotify_username"] = profiles.spotify_username
            context_dict["username"] = profiles.username

    if request.method == "POST":
        try:
            top_song = json.loads(request.body)
            context_dict["top_song"] = top_song
            for profiles in Profile.objects.all():
                if profiles.username == username:
                    profiles.top_song = top_song
                    profiles.save()

            return render(request, "rankedify/profile.html", context=context_dict)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    print("Context:" + context_dict["username"])
    return render(request, 'rankedify/profile.html', context=context_dict)

def view_profile(request, username_slug):
    context_dict = {}

    try:
        username = Profile.objects.get(slug=username_slug)
        profile = Profile.objects.get(username=username)

        try:
            file_path = profile.photo.path
            split = file_path.split('\\')
            path = split[-1]
        except ValueError:
            path = "default.jpg"

        context_dict['username'] = username
        context_dict['spotify_username'] = profile.spotify_username
        context_dict['photo'] = path
        print("photo: " + path)
        context_dict['favourite_song'] = profile.top_song
    except Profile.DoesNotExist:
        context_dict['username'] = None
        context_dict['spotify_username'] = None
        context_dict['photo'] = None
        context_dict['favourite_song'] = None

    print(is_friend(request, profile))
    context_dict['is_friend'] = is_friend(request, profile)

    return render(request, 'rankedify/userprofile.html', context=context_dict)

def is_friend(request, friend_profile):
    is_friend_bool = False

    try:
        Friends.objects.get(user1_id=request.user.id, user2_id=friend_profile.user.id)
        is_friend_bool = True
        print(is_friend_bool)
        return is_friend_bool
    except:
        try:
            Friends.objects.get(user1_id=friend_profile.user.id, user2_id=request.user.id)
            is_friend_bool = True
            print(is_friend_bool)
            return is_friend_bool
        except:
            is_friend_bool = False
            print(is_friend_bool)
            return is_friend_bool

def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("rankedify/users/username")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "rankedify/profile", {"form": form})



def friends(request):
    context_dict = {}
    context_dict['all_users'] = Profile.objects.order_by("username")
    friends_list = Friends.objects.filter(user1=request.user) | Friends.objects.filter(user2=request.user)
    friends_objects = []

    for friend in friends_list:
        for profiles in Profile.objects.all():
            if friend.user1_id == profiles.id and friend.user1_id != get_user_id(request):
                friends_objects.append(profiles)
                print(profiles.username)
            if friend.user2_id == profiles.id and friend.user2_id != get_user_id(request):
                friends_objects.append(profiles)
                print(profiles.username)

    context_dict['friends'] = friends_objects

    return render(request, "rankedify/friends.html", context=context_dict)

def signup(request):
    if request.method == "POST":

        username = request.POST.get('username')
        forename = request.POST.get('forename')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "rankedify/signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "rankedify/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return render(request, "rankedify/signup.html")
        
        user = Profile.objects.create_user(username=username, email=email, password=password, forename=forename, surname=surname, last_logged_in=(time.time()*1000))
        #user_profile = Profile.objects.create(forename=forename, surname=surname, user=user)

        user.save()
        #user_profile.save()

        login(request, user)
        return redirect('rankedifyapp:home')
    else:
        return render(request, "rankedify/signup.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('rankedifyapp:home') 
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('rankedifyapp:login')  
    else:
        return render(request, 'rankedify/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("rankedifyapp:home"))

def home(request):
    context_dict = {}
    if get_user_profile(request):
        context_dict['current_user_profile'] = Profile.objects.get(username=get_user_profile(request))
        context_dict['all_user_profiles'] = Profile.objects.order_by("-listening_minutes")
        print(f"{type(context_dict['current_user_profile'])}")
    else:
        context_dict['current_user_profile'] = None
        context_dict['all_user_profiles'] = None

    return render(request, "rankedify/home.html", context=context_dict)

@csrf_exempt
def add_friend(request):
    if request.method == "POST":
        context_dict = {}

        friend_username = json.loads(request.body)
        username = get_user_profile(request)

        user_profile = Profile.objects.get(username=username)
        friend_profile = Profile.objects.get(username=friend_username)

        for profiles in Profile.objects.all():
            if profiles.username == username:
                user_profile = profiles.profile

        for profiles in Profile.objects.all():
            if profiles.username == friend_username:
                friend_profile = profiles.profile

                try:
                    file_path = friend_profile.photo.path
                    split = file_path.split('\\')
                    path = split[-1]
                except ValueError:
                    path = "default.jpg"

                context_dict['username'] = friend_profile.username
                context_dict['spotify_username'] = friend_profile.spotify_username
                context_dict['photo'] = path

        if user_profile and friend_profile:
            if user_profile != friend_profile:
                new_friend = Friends.objects.create(user1=user_profile, user2=friend_profile)
                new_friend.save()

        context_dict['is_friend'] = is_friend(request, friend_profile)

        return render(request, 'rankedify/userprofile.html', context=context_dict)

def remove_friend(request):
    if request.method == "POST":
        context_dict = {}

        friend_username = json.loads(request.body)
        username = get_user_profile(request)

        user_profile = Profile.objects.get(username=username)
        friend_profile = Profile.objects.get(username=friend_username)

        for profiles in Profile.objects.all():
            if profiles.username == username:
                user_profile = profiles.profile

        for profiles in Profile.objects.all():
            if profiles.username == friend_username:
                friend_profile = profiles.profile

                try:
                    file_path = friend_profile.photo.path
                    split = file_path.split('\\')
                    path = split[-1]
                except ValueError:
                    path = "default.jpg"

                context_dict['username'] = friend_profile.username
                context_dict['spotify_username'] = friend_profile.spotify_username
                context_dict['photo'] = path

        if user_profile and friend_profile:
            friend_object = Friends.objects.get(user1=user_profile, user2=friend_profile) | Friends.objects.get(user2=user_profile, user1=friend_profile)
            friend_object.delete()

        context_dict['is_friend'] = is_friend(request, friend_profile)

        return render(request, 'rankedify/userprofile.html', context=context_dict)

def default_page(request):
    response = redirect("rankedify/home")
    return response

def error_page(request):
    return render(request, "rankedify/error-page.html")

def redirect_home(request):
    return render(request, "rankedify/home.html")

def get_spotify_data(request):
    return render(request, "rankedify/profile.html")

def get_user_profile(request):
    username = request.user.username
    return username



def get_user_id(request):
    id = request.user.id
    return id