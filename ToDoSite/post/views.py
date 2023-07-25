from django.shortcuts import render
from backend.Post import Post
from django.http import JsonResponse
from .models import post

def user_post(request):
    return Post.makePost(request)

def feed(request):
    posts = Post.getFeed(request)
    return render(request, 'post/feed.html', {"posts": posts})

def likes(request):
    return Post.userLike(request)


def create_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        message = request.POST.get("content")
        Original_post = post.objects.get(id=post_id)
        post.objects.create(user=request.user, text=message, tag=Original_post.tag, referenced_post=Original_post)
        return JsonResponse({'message': "success"});   
    return JsonResponse({'error': 'Invalid request.'}, status=400)


def comments(request, post_id):
    comments = Post.getComments(request, post_id)
    main = comments.last()
    comments = comments.exclude(id=main.id)
    return render(request, 'post/comment.html', {'main': main, 'comments':comments})