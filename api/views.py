from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "title": "Weather Site API"
    }
    return render(request, "index.html", context)