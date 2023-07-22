from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from post.models import post
from django.db.models import Count

# Create your views here.
def trending(request):
    one_hour_ago = timezone.now() - timedelta(hours=2)
    top_categories = post.objects.filter(time__gte=one_hour_ago).values('tag').annotate(post_count=Count('id'))
    top_categories = top_categories.order_by('-post_count')
    top_10_categories = top_categories[:10]

    return render(request, 'trending/trending.html', {"categories":top_10_categories})

def topic(request, topic):
    return render(request, 'trending/trending.html', {"posts":posts})