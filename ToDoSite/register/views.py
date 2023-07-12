from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUser

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.success(request, 'The details were incorrect please try again')
            return render(request, 'register/login.html', {})
    else:
        return render(request, 'register/login.html', {})
    


def register_user(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username, password)
            login(request, user)
            messages.success("request", ("Registration was successful"))
    else:
        form = RegisterUser()    
    return render(request, 'register/register.html', {"form": form})

def logout_user(request):
    logout(request)
    return redirect('/login/')