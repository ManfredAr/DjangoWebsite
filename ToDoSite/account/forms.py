from django import forms
from .models import Profile

class ChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'description']