from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.explore),
    path('<str:username>', views.person),
    path('<str:username>/followers', views.followers),
    path('<str:username>/following', views.following),
    path('follow-unfollow/', views.checkFollow),
]