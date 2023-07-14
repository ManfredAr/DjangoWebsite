from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.explore),
    path('<str:username>', views.person)
]