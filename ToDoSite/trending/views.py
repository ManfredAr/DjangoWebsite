from django.shortcuts import render
from backend.Post import Post
from backend.trends import trends

# Create your views here.
def trending(request):
    return trends.trending(request)

def getTopicPosts(request, topic):
    posts = Post.getTopicPosts(request, topic)
    return render(request, 'trending/topic.html', {"topic":topic, "posts":posts})