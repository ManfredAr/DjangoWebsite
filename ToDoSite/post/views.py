from django.shortcuts import render, redirect
from .models import post, like
from account.models import follower
from django.contrib import messages
from django.db.models import When, Case, BooleanField, F
from django.http import JsonResponse


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
        post_id = request.POST.get("form_id")
        post_obj = post.objects.get(id=post_id)
        user_like = True;
        button = "like-count-" + post_id
        if (like.objects.filter(post=post_obj, user=request.user).exists()):
            user_like = False
            like_obj = like.objects.get(post_id=post_id, user_id=request.user.id)
            like_obj.delete()
            post_obj.likes = like.objects.filter(post_id=post_id).count()
            post_obj.save()
        else:
            like.objects.create(post=post_obj, user=request.user)
            post_obj.likes = like.objects.filter(post_id=post_id).count()
            post_obj.save()

        # Return a JSON response indicating success
        return JsonResponse({'like_count': post_obj.likes, 'user_like': user_like, 'id': button, 'post_id':post_id})

    # Return a JSON response indicating error
    return JsonResponse({'error': 'Invalid request.'}, status=400)