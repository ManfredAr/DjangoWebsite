from django.shortcuts import render, redirect
from account.models import Profile
from account.models import follower
from backend.Post import Post
from django.contrib.auth.models import User


class profiles:

    @staticmethod
    def getProfile(request):
        '''
        Returns all the posts, followers and followings of a user.
        '''

        # Gets all the posts made by the user.
        posts = Post.getPost(request, request.user)

        # Gets the profile image and descriptiob of the user
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=request.user)
        else:
            profile = Profile.objects.create(user_id=request.user.id, image="account-images/default.jpg", description="")

        # Gets the number followers and following users.
        followers = follower.objects.filter(followee=request.user).count
        following = follower.objects.filter(follower=request.user).count
        return render(request, 'account/profile.html', {'posts': posts, "profile":profile, "followers":followers, "following":following}) 
    

    @staticmethod
    def changeProfile(request):
        '''
        This methods changes a users profile image, description or both.
        '''

        if request.method == 'POST':
            #Retrieve the users original profile.
            profile = Profile.objects.get(user=request.user)

            # Get the new image and description and update teh profile.
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
        '''
        Returns all the posts, followers and followings of another user.
        '''

        #Retrieves the posts made by the user
        user_details = User.objects.get(username=username)
        Posts = Post.getPost(request, user_details)

        #Gets the following and followers count.
        followers = follower.objects.filter(followee=user_details).count
        following = follower.objects.filter(follower=user_details).count

        #Gets the profle image and description.
        if Profile.objects.filter(user=user_details).exists():
            profile = Profile.objects.get(user=user_details)
        else:
            profile = Profile.objects.create(user_id=user_details.id, image="account-images/default.jpg", description="")

        # Gets whether the authenticated user follows this user or not.
        is_following = follower.objects.filter(follower=request.user, followee=user_details).exists()
        return render(request, 'explore/person.html', {"profile":profile, "person": user_details, "posts": Posts, "follow": is_following, "followers":followers, "following":following})
