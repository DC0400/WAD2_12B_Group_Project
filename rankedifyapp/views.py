from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import redirect


def index(request):
    leaderboard = Profile.objects.order_by("-total_minutes_listened")[:12] 
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
            #print("Received Top Tracks:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)

def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("rankedfiy/users/username")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "rankedify/profile", {"form": form})




def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "rankedify/signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "rankedify/signup.html")
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('rankedify:home')
    else:
        return render(request, "rankedify/signup.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('rankedify:home')
        else:
            return HttpResponse("Invalid login")
    
    return render(request, 'rankedify/login.html')

def user_logout(request):
    logout(request)
    return redirect('rankedify:home')

def home(request):
    return render(request, "rankedify/home.html")

def default_page(request):
    response = redirect("rankedify/home")
    return response