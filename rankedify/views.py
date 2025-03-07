from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'rankedify/index.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_tracks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Top Tracks:", data)
            return JsonResponse({"message": "Data received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)