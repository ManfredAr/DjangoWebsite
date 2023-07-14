from django.shortcuts import render
from post.models import post

# Create your views here.
def profile(request):
    Posts = post.objects.filter(user=request.user).order_by('-time')
    return render(request, 'account/profile.html', {'posts': Posts}) 