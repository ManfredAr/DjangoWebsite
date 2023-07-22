import os
from django.shortcuts import render, redirect
from post.models import post
from .models import Profile
from .forms import ChangeForm
from .models import follower
from backend.Post import Post

# Create your views here.
def profile(request):
    posts = Post.getPost(request, request.user)
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
    else:
        profile = Profile.objects.create(user_id=request.user.id, image="account-images/default.jpg", description="")
    followers = follower.objects.filter(followee=request.user).count
    following = follower.objects.filter(follower=request.user).count
    return render(request, 'account/profile.html', {'posts': posts, "profile":profile, "followers":followers, "following":following}) 

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
        image_name = os.path.basename(profile.image.name) if profile and profile.image else None
        return render(request, 'account/changeProfile.html', {'form': form, 'image_name': image_name})
    return render(request, 'account/changeProfile.html', {'form': form, 'image_name': image_name})