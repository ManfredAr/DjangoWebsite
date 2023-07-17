from django.shortcuts import render, redirect
from .models import post
from account.models import follower
from django.contrib import messages

# Create your views here.
def user_post(request):
    if request.method == "POST":
        content = request.POST['content']
        if content == '':
            messages.success(request, ("The post is empty please enter something"))
            return redirect('/post/')
        else:
            newpost = post(user=request.user, text=content)
            newpost.save()
            return redirect('/home/')
    return render(request, 'post/post.html', {})

def feed(request):
    following = follower.objects.filter(follower=request.user)
    following_users = [entry.followee for entry in following]
    posts = post.objects.filter(user__in=following_users).order_by('-time')
    return render(request, 'post/feed.html', {"posts": posts})