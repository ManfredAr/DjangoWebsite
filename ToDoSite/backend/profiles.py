from django.shortcuts import render, redirect
from account.models import Profile
from account.forms import ChangeForm
from account.models import follower
from backend.Post import Post
from django.contrib.auth.models import User


class profiles:

    @staticmethod
    def getProfile(request):
        posts = Post.getPost(request, request.user)
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=request.user)
        else:
            profile = Profile.objects.create(user_id=request.user.id, image="account-images/default.jpg", description="")
        followers = follower.objects.filter(followee=request.user).count
        following = follower.objects.filter(follower=request.user).count
        return render(request, 'account/profile.html', {'posts': posts, "profile":profile, "followers":followers, "following":following}) 
    
    @staticmethod
    def changeProfile(request):
        if request.method == 'POST':
            profile = Profile.objects.get(user=request.user)
            profile.image = request.POST.get("image_choice")
            profile.description = request.POST.get('desc')
            profile.save()
            return redirect('/profile/')
        else:
            profile = Profile.objects.get(user=request.user)
            current_image = profile.image
            current_desc = profile.description
            options = ['1_image.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.png', 'default.jpg']
            return render(request, 'account/changeProfile.html', {'desc': current_desc, 'img': current_image, 'options': options})

    
    @staticmethod
    def getPersonProfile(request, username):
        user_details = User.objects.get(username=username)
        Posts = Post.getPost(request, user_details)
        followers = follower.objects.filter(followee=user_details).count
        following = follower.objects.filter(follower=user_details).count
        if Profile.objects.filter(user=user_details).exists():
            profile = Profile.objects.get(user=user_details)
        else:
            profile = Profile.objects.create(user_id=user_details.id, image="account-images/default.jpg", description="")
        

        if (request.method == "POST"):
            choice = request.POST["choice"]
            if (choice == "follow"):
                follower.objects.create(follower=request.user, followee=user_details)
            else:
                follower_entry = follower.objects.filter(follower=request.user, followee=user_details)
                if follower_entry:
                    follower_entry.delete()

        is_following = follower.objects.filter(follower=request.user, followee=user_details).exists()
        return render(request, 'explore/person.html', {"profile":profile, "person": user_details, "posts": Posts, "follow": is_following, "followers":followers, "following":following})
