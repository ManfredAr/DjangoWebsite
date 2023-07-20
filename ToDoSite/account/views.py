from django.shortcuts import render, redirect
from post.models import post
from .models import Profile
from .forms import ChangeForm

# Create your views here.
def profile(request):
    Posts = post.objects.filter(user=request.user).order_by('-time')
    profile = Profile.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'posts': Posts, "profile":profile}) 

def changeProfile(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST, request.FILES)
        if form.is_valid():
            if Profile.objects.filter(user=request.user).exists():
                profile = Profile.objects.get(user=request.user)
                profile.image = form.cleaned_data['image']
                profile.description = form.cleaned_data['description']
                profile.save()
            else:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()

            return redirect('/profile/')
    else:
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=request.user)
            form = ChangeForm(instance=profile)
        else:
            form = ChangeForm()

    return render(request, 'account/changeProfile.html', {'form': form})