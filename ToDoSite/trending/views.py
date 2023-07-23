from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from post.models import post
from django.db.models import Count
from backend.Post import Post
import re

# Create your views here.
def trending(request):
    one_hour_ago = timezone.now() - timedelta(hours=2)
    top_categories = post.objects.filter(time__gte=one_hour_ago).values('tag').annotate(post_count=Count('id'))
    top_categories = top_categories.order_by('-post_count')
    top_10_categories = top_categories[:10]

    if request.method == "POST":
        search = request.POST['search']
        print(search)
        if search[0:1] == "#":
            posts = Post.getTopicPosts(request, search[1:])
            return render(request, 'trending/topic.html', {"topic":search[1:], "posts":posts})
        else:
            posts = Post.getSearchPosts(request, search[1:])
            return render(request, 'trending/topic.html', {"topic":search, "posts":posts})

    return render(request, 'trending/trending.html', {"categories":top_10_categories})

def getTopicPosts(request, topic):
    posts = Post.getTopicPosts(request, topic)
    return render(request, 'trending/topic.html', {"topic":topic, "posts":posts})