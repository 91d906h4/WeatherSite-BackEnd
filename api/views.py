from django.http.response import JsonResponse
from django.shortcuts import render
from .functions.get_weather import *

# Create your views here.

def index(request, id):
    weather_data = get_weather_data("466950")[1] # C0A86 466950
    data = {
        "title": "Weather Site API",
        "method": request.method,
        "id": id,
        "data": weather_data
    }
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})