from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return HttpResponse("this is home")