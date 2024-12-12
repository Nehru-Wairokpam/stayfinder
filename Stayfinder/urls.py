"""
URL configuration for Stayfinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from StayfinderApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('toptenroomlist/', views.topTenRoomList,  name='topTenRoomList'),
    path('pickedoftheday/', views.pickedoftheday,  name='pickedoftheday'),
    path('hotel/', views.hotel,  name='hotel'),
    path('hotelDetails/', views.hotel_Details),
    path('roomDetails/', views.room_Details),
    path('search/', views.search),
    path('signUp/', views.signUp, name='signUp'),
    path('signup_post/', views.signup_post, name='signup_post'),
    path('login', views.login, name='login'),
    path('login_post/', views.login_post, name='login_post'),

]

