from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def default_page(request):
    response = redirect('/rankedify/home')
    return response

def home(request):
    return HttpResponse("this is home")