from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUser(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']