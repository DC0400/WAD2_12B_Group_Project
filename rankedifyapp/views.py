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
from .models import Profile
from django.shortcuts import redirect

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
                    profiles.save()

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
                    print(data)
                    profiles.spotify_username = data
                    profiles.save()

            #print("Received Profile:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

def profile(request):
    return render(request, 'rankedify/profile.html')

def view_profile(request, username_slug):
    context_dict = {}

    try:
        username = Profile.objects.get(slug=username_slug)
        profile = Profile.objects.get(username=username)

        file_path = profile.photo.path
        split = file_path.split('\\')
        path = split[-1]

        context_dict['username'] = username
        context_dict['spotify_username'] = profile.spotify_username
        context_dict['photo'] = path
        print("photo: " + path)
        #context_dict['favourite_song'] = profile.favourite_song
    except Profile.DoesNotExist:
        context_dict['username'] = None
        context_dict['spotify_username'] = None
        context_dict['photo'] = None
        #context_dict['favourite_song'] = None

    return render(request, 'rankedify/userprofile.html', context=context_dict)

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
    return render(request, "rankedify/friends.html")

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
        
        if user:
            login(request, user)
            return redirect('rankedifyapp:home')
        else:
            return HttpResponse("Invalid login")
    
    return render(request, 'rankedify/login.html')

def user_logout(request):
    logout(request)
    return redirect('rankedify:home')

def home(request):
    context_dict = {}
    context_dict['current_user_profile'] = Profile.objects.get(username=get_user_profile(request))
    context_dict['all_user_profiles'] = Profile.objects.order_by("-listening_minutes")
    print(f"{type(context_dict['current_user_profile'])}")

    return render(request, "rankedify/home.html", context=context_dict)

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