from django.shortcuts import render
from django.contrib.auth.models import User
import json

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})