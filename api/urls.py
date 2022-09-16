from django.urls import path
from . import views

urlpatterns = [
    path('get/<str:city>', views.get_city, name="Get"),
    path('<str:key>/<str:id>', views.get, name="Index"),
]