from django.shortcuts import render
from backend.Post import Post
from backend.comment import comment
from backend.userLikes import userLikes
from django.http import JsonResponse

def user_post(request):
    return Post.makePost(request)

def feed(request):
    if request.user.is_authenticated:
        posts = Post.getFeed(request)
        return render(request, 'post/feed.html', {"posts": posts})
    else: 
        return render(request, 'post/feed.html', {})

def likes(request):
    return userLikes.userLike(request)


def create_comment(request):
    if request.method == "POST":
        comment.createComment(request)
        return JsonResponse({'message': "success"});   
    return JsonResponse({'error': 'Invalid request.'}, status=400)


def comments(request, post_id):
    if request.user.is_authenticated:
        comments = comment.getComments(request, post_id)
        main = comments.last()
        comments = comments.exclude(id=main.id)
        return render(request, 'post/comment.html', {'main': main, 'comments':comments})
    else:
        return render(request, 'post/comment.html', {})