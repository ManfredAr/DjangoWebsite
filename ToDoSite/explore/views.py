from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import post
import json
from account.models import follower
from backend.Post import Post
from account.models import Profile
from django.db.models import Subquery, OuterRef

# Create your views here.
def explore(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, 'explore/explore.html', {"username":usernames})

def person(request, username):
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

def followers(request, username):
    profile = User.objects.get(username=username)
    followers = follower.objects.filter(followee=profile)
    follower_users = [follower.follower for follower in followers]
    profiles = Profile.objects.filter(user__in=follower_users)
    followers = followers.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('follower')).values('image')[:1]))
    print(followers[0].creator_profile_image)
    return render(request, 'explore/followers.html', {"profile": profile, "followers": followers})


def following(request, username):
    profile = User.objects.get(username=username)
    followers = follower.objects.filter(follower=profile)
    follower_users = [follower.followee for follower in followers]
    profiles = Profile.objects.filter(user__in=follower_users)
    following = followers.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('followee')).values('image')[:1]))
    print(following[0].creator_profile_image)
    return render(request, 'explore/following.html', {"profile":profile, "following":following})