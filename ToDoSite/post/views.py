from django.shortcuts import render, redirect
from .models import post
from django.contrib import messages

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