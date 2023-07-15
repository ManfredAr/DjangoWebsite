from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import post
import json
from account.models import follower

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})

def person(request, username):
    user_details = User.objects.get(username=username)
    Posts = post.objects.filter(user=user_details).order_by('-time')
    
    if (request.method == "POST"):
        choice = request.POST["choice"]
        if (choice == "follow"):
            follower.objects.create(follower=request.user, followee=user_details)
        else:
            follower_entry = follower.objects.filter(follower=request.user, followee=user_details)
            if follower_entry:
                follower_entry.delete()

    is_following = follower.objects.filter(follower=request.user, followee=user_details).exists()
    return render(request, 'explore/person.html', {"profile": user_details, "posts": Posts, "follow": is_following})