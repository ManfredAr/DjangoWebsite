from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import post
import json
from account.models import follower
from backend.Post import Post
from account.models import Profile
from django.db.models import Subquery, OuterRef

class follows:

    @staticmethod
    def following(request, username):
        profile = User.objects.get(username=username)
        followers = follower.objects.filter(follower=profile)
        follower_users = [follower.followee for follower in followers]
        profiles = Profile.objects.filter(user__in=follower_users)
        following = followers.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('followee')).values('image')[:1]))
        print(following[0].creator_profile_image)
        return render(request, 'explore/following.html', {"profile":profile, "following":following})
    

    def followers(request, username):
        profile = User.objects.get(username=username)
        followers = follower.objects.filter(followee=profile)
        follower_users = [follower.follower for follower in followers]
        profiles = Profile.objects.filter(user__in=follower_users)
        followers = followers.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('follower')).values('image')[:1]))
        print(followers[0].creator_profile_image)
        return render(request, 'explore/followers.html', {"profile": profile, "followers": followers})