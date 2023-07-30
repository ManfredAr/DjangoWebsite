from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from register.forms import RegisterUser

class verify:

    @staticmethod
    def login(request):
        '''
        Checks the details entered by a user to allow access.
        '''

        #retrieves the username and password entered.
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        #If corrent then allow access
        if user is not None:
            login(request, user)
            return redirect('/post/feed')
        else:
            messages.success(request, 'The details were incorrect please try again')
            return render(request, 'register/login.html', {})
        
    
    @staticmethod
    def register(request):
        '''
        Creates a new user if the registration details are acceptable.
        '''
        if request.method == "POST":
            form = RegisterUser(request.POST)
            if form.is_valid():
                form.save()
                # retrives the username and password and creates a new user.
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect(request, '/post/feed/', {})
        form = RegisterUser()    
        return render(request, 'register/register.html', {"form": form})