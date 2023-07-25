from django.urls import path, include
from . import views

urlpatterns = [
    path('post/', views.user_post),
    path('feed/', views.feed),
    path('input-likes', views.likes),
    path('create-comment', views.create_comment),
    path('<int:post_id>', views.comments, name='comments'),
]