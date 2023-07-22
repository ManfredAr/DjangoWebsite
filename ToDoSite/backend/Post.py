from django.shortcuts import render, redirect
from post.models import post, like
from account.models import follower, Profile
from django.contrib import messages
from django.db.models import Subquery, OuterRef, Exists
from django.http import JsonResponse


class Post:

    @staticmethod
    def makePost(request):
        if request.method == "POST":
            content = request.POST['content']
            content = content.replace('\n', '<br>')
            tag = request.POST['tag']
            tag = tag.replace(" ", "").lower()
            newpost = post(user=request.user, text=content, tag=tag)
            newpost.save()
            return redirect('/home/')
        return render(request, 'post/post.html', {})

    @staticmethod
    def getFeed(request):
        following = follower.objects.filter(follower=request.user)
        following_users = [entry.followee for entry in following]

        # Get posts made by people the user follows
        posts = post.objects.filter(user__in=following_users).order_by('-time')

        # Annotate the 'user_like' field to indicate if the authenticated user has liked each post
        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(user_like=Exists(user_likes))

        # Annotate the 'creator_profile_image' field to get the profile picture of the post creator
        profiles = Profile.objects.filter(user__in=Subquery(posts.values('user')))
        posts = posts.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('user')).values('image')[:1]))
        return posts



    @staticmethod
    def getPost(request, who):
        posts = post.objects.filter(user=who).order_by('-time')
        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(user_like=Exists(user_likes))
        posts = posts.distinct()
        return posts
    

    
    @staticmethod
    def userLike(request):
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
    
    @staticmethod
    def getTopicPosts(request, topic):
        posts = post.objects.filter(tag=topic).order_by('-time')

        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(user_like=Exists(user_likes))

        profiles = Profile.objects.filter(user__in=Subquery(posts.values('user')))
        posts = posts.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('user')).values('image')[:1]))
        return posts