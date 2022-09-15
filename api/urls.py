from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('<str:id>', views.get, name="Index"),
]