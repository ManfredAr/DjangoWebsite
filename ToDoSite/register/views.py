from django.shortcuts import render
from django.contrib.auth import authentication
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/home/')
        else:
            messages.success(request, ("There was an error logging in try again"))
            return redirect('http://127.0.0.1:8000/home/')

    return render(request, 'registration/login.html' {})