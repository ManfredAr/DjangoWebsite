from django.shortcuts import render, redirect
from .models import post, like
from account.models import follower
from django.contrib import messages
from django.db.models import When, Case, BooleanField, F

# Create your views here.
def user_post(request):
    if request.method == "POST":
        content = request.POST['content']
        if content == '':
            messages.success(request, ("The post is empty please enter something"))
            return redirect('/post/')
        else:
            newpost = post(user=request.user, text=content)
            newpost.save()
            return redirect('/home/')
    return render(request, 'post/post.html', {})


def feed(request):
    following = follower.objects.filter(follower=request.user)
    following_users = [entry.followee for entry in following]
    posts = post.objects.filter(user__in=following_users).order_by('-time')
    posts = posts.annotate(user_like=Case(
            When(like__user=request.user, then=True),
            default=False,
            output_field=BooleanField()
    ))
    return render(request, 'post/feed.html', {"posts": posts})

def likes(request):
    if request.method == "POST":
        choice = request.POST.get("is-liked")
        postid = request.POST.get("post_id")
        posts = post.objects.get(id=postid)
        if choice == "like":
            like.objects.create(post_id=posts.id, user=request.user)
            post.objects.filter(id=postid).update(likes=F('likes') + 1)
        else:
            like.objects.get(post_id=posts, user=request.user).delete()
            post.objects.filter(id=postid).update(likes=F('likes') - 1)
    return feed(request)
