from django.urls import path
from . import views

urlpatterns = [
    path('', views.trending),
    path('<str:topic>', views.getTopicPosts),
]