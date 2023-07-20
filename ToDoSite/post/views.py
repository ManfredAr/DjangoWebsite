from django.shortcuts import render
from backend.Post import Post

def user_post(request):
    return Post.makePost(request)

def feed(request):
    posts = Post.getFeed(request)
    return render(request, 'post/feed.html', {"posts": posts})

def likes(request):
    return Post.userLike(request)