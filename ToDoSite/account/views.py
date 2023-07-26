from backend.profiles import profiles

# Create your views here.
def profile(request):
    return profiles.getProfile(request)

def changeProfile(request):
    return profile.changeProfile(request)