from django import forms
from .models import post

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['text', 'tag']
        #fields = ['text', 'tag', 'image']

        
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 100}),
            'tag': forms.TextInput(attrs={'size': 30}),
        }