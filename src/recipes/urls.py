from django.urls import path
from .views import home

app_name = "recipes"

urlpatterns = [
    path("", home),
]