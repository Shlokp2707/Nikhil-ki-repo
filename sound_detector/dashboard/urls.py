from django.contrib import admin
from django.urls import path,include
from .views import udashboard
urlpatterns = [
    path('dashboard/',udashboard,name="dashboard")
]