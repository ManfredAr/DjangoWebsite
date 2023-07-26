from django.shortcuts import render
from django.contrib.auth.models import User
from backend.follows import follows
from backend.profiles import profiles

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})

def person(request, username):
    return profiles.getPersonProfile(request, username)

def followers(request, username):
    return follows.followers(request, username)

def following(request, username):
    return follows.following(request, username)