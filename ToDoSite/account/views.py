from backend.profiles import profiles
from django.shortcuts import render

# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        return profiles.getProfile(request)
    return render(request, 'account/profile.html', {}) 
    

def changeProfile(request):
    if request.user.is_authenticated:
        return profiles.changeProfile(request)
    return render(request, 'account/changeProfile.html', {})