from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegisterUser
from backend.verify import verify


def login_user(request):
    if request.method == "POST":
        return verify.login(request)
    else:
        return render(request, 'register/login.html', {})
    


def register_user(request):
    if request.method == "POST":
        verify.register(request)
    else:
        form = RegisterUser()    
    return render(request, 'register/register.html', {"form": form})



def logout_user(request):
    logout(request)
    return redirect('/login/')
