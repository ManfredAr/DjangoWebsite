from django.shortcuts import render, redirect
from post.models import post, like
from account.models import follower, Profile
from django.db.models import Subquery, OuterRef, Exists, Count, F


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
        
