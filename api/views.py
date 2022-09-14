from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    if(request.method == "GET"):
        method = request.method
    data = {
        "title": "Weather Site API",
        "method": method
    }
    return JsonResponse(data)