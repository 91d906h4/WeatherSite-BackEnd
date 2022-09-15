from django.http.response import JsonResponse, HttpResponse
from .functions.get_weather import *

# Create your views here.

def get(request, key, id):
    if int(key) % 104729 == 0:
        data = get_weather_data(id) # C0A770 466950
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else: return JsonResponse({"status": "error", "message": "Incorrect API key."}, safe=False, json_dumps_params={'ensure_ascii': False})