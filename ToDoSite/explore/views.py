from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import post
import json
from account.models import follower
from backend.Post import Post

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})

def person(request, username):
    user_details = User.objects.get(username=username)
    Posts = Post.getPost(request, user_details)
    followers = follower.objects.filter(followee=user_details)
    following = follower.objects.filter(follower=user_details)
    

    if (request.method == "POST"):
        choice = request.POST["choice"]
        if (choice == "follow"):
            follower.objects.create(follower=request.user, followee=user_details)
        else:
            follower_entry = follower.objects.filter(follower=request.user, followee=user_details)
            if follower_entry:
                follower_entry.delete()

    is_following = follower.objects.filter(follower=request.user, followee=user_details).exists()
    return render(request, 'explore/person.html', {"profile": user_details, "posts": Posts, "follow": is_following, "followers":followers, "following":following})

def followers(request, username):
    profile = User.objects.get(username=username)
    followers = follower.objects.filter(followee=profile)
    return render(request, 'explore/followers.html', {"profile":profile, "followers":followers})

def following(request, username):
    profile = User.objects.get(username=username)
    following = follower.objects.filter(follower=profile)
    return render(request, 'explore/following.html', {"profile":profile, "following":following})