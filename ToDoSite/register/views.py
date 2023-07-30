from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegisterUser
from backend.verify import verify
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from register.forms import RegisterUser



def login_user(request):
    if request.method == "POST":
        return verify.login(request)
    else:
        return render(request, 'register/login.html', {})
    


def register_user(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/post/feed/')
    form = RegisterUser()    
    return render(request, 'register/register.html', {"form": form})



def logout_user(request):
    logout(request)
    return redirect('/login/')
