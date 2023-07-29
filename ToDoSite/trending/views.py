from django.shortcuts import render
from backend.Post import Post
from backend.trends import trends

# Create your views here.
def trending(request):
    if request.user.is_authenticated:
        return trends.trending(request)
    else:
        return render(request, 'trending/trending.html', {})

def getTopicPosts(request, topic):
    if request.user.is_authenticated:
        posts = Post.getTopicPosts(request, topic)
        return render(request, 'trending/topic.html', {"topic":topic, "posts":posts})
    else:
        return render(request, 'trending/topic.html', {})