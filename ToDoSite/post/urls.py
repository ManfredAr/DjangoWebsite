from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('post/', views.user_post),
    path('feed/', views.feed),
]