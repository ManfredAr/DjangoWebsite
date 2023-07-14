from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import post
import json

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})

def person(request, username):
    user_details = User.objects.get(username=username)
    Posts = post.objects.filter(user=user_details).order_by('-time')
    return render(request, 'explore/person.html', {"user": user_details, "posts": Posts})