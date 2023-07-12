from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, "home/home.html", {})
    else:
        return render(request, "register/login.html", {})
        
        
