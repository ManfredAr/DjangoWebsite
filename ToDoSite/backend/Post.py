from django.shortcuts import render, redirect
from post.models import post, like
from account.models import follower, Profile
from django.db.models import Subquery, OuterRef, Exists, Count, F
from post.forms import PostForm
from django.contrib.auth.models import User
from account.models import follower
import os
import uuid


class Post:

    @staticmethod
    def makePost(request):
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                text = form.cleaned_data['text']
                tag = form.cleaned_data['tag']
                #image = form.cleaned_data['image']
                #image.image = Post.get_unique_filename(image)
                text = text.replace('\n', '<br>')
                tag = tag.replace(" ", "").lower()
                newpost = post(user=request.user, text=text, tag=tag)
                #newpost = post(user=request.user, text=text, tag=tag, image=image)
                newpost.save()
                return redirect('/home/')
        form = PostForm()
        return render(request, 'post/post.html', {'form':form})
    

    #def get_unique_filename(filename):
        # Generate a random unique string using UUID (Universally Unique Identifier)
        unique_name = str(uuid.uuid4())

        # Get the file extension from the original filename
        ext = os.path.splitext(filename)[1]

        # Combine the unique string and the file extension to create the new filename
        new_filename = unique_name + ext
        return new_filename


    @staticmethod
    def getFeed(request):
        '''
        Method returns all the posts made by users followed. It includes the post, 
        comment count, like count and also if the user has like the post or not.
        '''
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

        # Annotate the 'comment_count' field to get the number of comments for each post
        comment_counts = post.objects.filter(referenced_post=OuterRef('pk')).values('pk').annotate(comment_count=Count('pk'))
        posts = posts.annotate(comment_count=Subquery(comment_counts.values('comment_count')))

        referenced_posts = post.objects.filter(id=OuterRef('referenced_post')).values('text', 'id')
        posts = posts.annotate(referenced_post_pk=Subquery(referenced_posts.values('id')[:1]))
        return posts


    @staticmethod
    def getTopUsers(request):
        users_with_most_followers = follower.objects.values('followee').annotate(num_followers=Count('followee')).order_by('-num_followers')[:5]
        user_ids = [user['followee'] for user in users_with_most_followers]
        top_users = User.objects.filter(id__in=user_ids)
        profiles = Profile.objects.filter(user__in=user_ids)
        top_users = top_users.annotate(p_image=Subquery(profiles.filter(user=OuterRef('id')).values('image')[:1]))
        top_users = top_users.annotate(p_desc=Subquery(profiles.filter(user=OuterRef('id')).values('description')[:1]))
        return render(request, 'post/feed.html', {"top_users": top_users})


    @staticmethod
    def getPost(request, who):
        comment_counts = post.objects.filter(referenced_post=OuterRef('pk')).values('pk').annotate(comment_count=Count('pk'))

        # Annotate the comment_count field to get the number of comments for each post
        posts = post.objects.filter(user=who).order_by('-time')
        posts = posts.annotate(user_like=Exists(like.objects.filter(user=request.user, post=OuterRef('pk'))))
        posts = posts.distinct()
        posts = posts.annotate(comment_count=Subquery(comment_counts.values('comment_count')))

        # Annotate the referenced_post for each comment post
        referenced_posts = post.objects.filter(id=OuterRef('referenced_post')).values('text', 'id')
        posts = posts.annotate(referenced_post_pk=Subquery(referenced_posts.values('id')[:1]))
        return posts
    
    @staticmethod
    def getTopicPosts(request, topic):
        posts = post.objects.filter(tag=topic).order_by('-time')

        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(user_like=Exists(user_likes))

        profiles = Profile.objects.filter(user__in=Subquery(posts.values('user')))
        posts = posts.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('user')).values('image')[:1]))
        referenced_posts = post.objects.filter(id=OuterRef('referenced_post')).values('text', 'id')
        posts = posts.annotate(referenced_post_pk=Subquery(referenced_posts.values('id')[:1]))
        comment_counts = post.objects.filter(referenced_post=OuterRef('pk')).values('pk').annotate(comment_count=Count('pk'))
        posts = posts.annotate(comment_count=Subquery(comment_counts.values('comment_count')))
        return posts
    
    @staticmethod
    def getSearchPosts(request, search):
        posts = post.objects.filter(text__icontains=search).order_by('-time')

        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(user_like=Exists(user_likes))

        profiles = Profile.objects.filter(user__in=Subquery(posts.values('user')))
        posts = posts.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('user')).values('image')[:1]))
        referenced_posts = post.objects.filter(id=OuterRef('referenced_post')).values('text', 'id')
        posts = posts.annotate(referenced_post_pk=Subquery(referenced_posts.values('id')[:1]))
        comment_counts = post.objects.filter(referenced_post=OuterRef('pk')).values('pk').annotate(comment_count=Count('pk'))
        posts = posts.annotate(comment_count=Subquery(comment_counts.values('comment_count')))
        return posts
        
