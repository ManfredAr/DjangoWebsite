from django.shortcuts import render
from django.contrib.auth.models import User
from backend.follows import follows
from backend.profiles import profiles
from post.models import post
from account.models import Profile
from django.db.models import Subquery, OuterRef


# Create your views here.
def explore(request):
    if request.method == "POST":
        search = request.POST.get("query")
        if search[0:1] == "#":
            matching_tags = post.objects.filter(tag__icontains=search[1:]).values_list('tag', flat=True).distinct()
            return render(request, 'explore/explore.html', {'tags': matching_tags, 'search':search, 'expect_Tag':True})
        else:
            matching_users = User.objects.filter(username__icontains=search)
            profiles = Profile.objects.filter(user__in=matching_users)
            matching_users = matching_users.annotate(p_image=Subquery(profiles.filter(user=OuterRef('id')).values('image')[:1]))
            matching_users = matching_users.annotate(p_desc=Subquery(profiles.filter(user=OuterRef('id')).values('description')[:1]))
            return render(request, 'explore/explore.html', {'users': matching_users, 'search':search, 'expect_User':True})
    return render(request, 'explore/explore.html', {})

def person(request, username):
    if request.user.is_authenticated:
        return profiles.getPersonProfile(request, username)
    else:
        return render(request, 'account/profile.html', {}) 

def followers(request, username):
    if request.user.is_authenticated:
        return follows.followers(request, username)
    else:
        return render(request, 'explore/followers.html', {})

def following(request, username):
    if request.user.is_authenticated:
        return follows.following(request, username)
    else:
        return render(request, 'explore/following.html', {})