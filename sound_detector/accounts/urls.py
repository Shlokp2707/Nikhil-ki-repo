from django.contrib import admin
from django.urls import path
from .views import ulogin,usignup
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ulogin,name ='login'),
    path('signup/',usignup,name='signup')
    ]