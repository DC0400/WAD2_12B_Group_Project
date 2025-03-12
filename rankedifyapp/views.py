from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def default_page(request):
    response = redirect('/rankedify/home')
    return response

def home(request):
    return render(request, 'rankedify/home.html')

def signup(request):
    return render(request, 'rankedify/signup.html')