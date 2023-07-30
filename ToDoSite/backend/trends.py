from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from post.models import post
from django.db.models import Count
from backend.Post import Post
from django.http import JsonResponse

class trends:

    @staticmethod
    def trending(request):
        if request.method == "POST":
            '''
            Gets the top 10 tags along with the number of posts made with that tag in the last hour or all time.
            '''

            choice = request.POST.get('button')
            if choice == 'hour':
                time = timezone.now() - timedelta(hours=1)
                #Retrieves the top 10 tags in the last hour.
                top_categories = post.objects.filter(time__gte=time).values('tag').annotate(post_count=Count('id'))
                top_categories = top_categories.order_by('-post_count')
                top_10_categories = top_categories[:10]
                return JsonResponse({'categories': list(top_10_categories), 'hour': True})
            else:
                #Retrieves the top 10 tags of all time.
                top_10_categories = post.objects.values('tag').annotate(post_count=Count('tag')).order_by('-post_count')[:10]
                top_10_categories = top_10_categories[:10]
                return JsonResponse({'categories': list(top_10_categories)})
        
        # By default its set to all time.
        top_10_categories = post.objects.values('tag').annotate(post_count=Count('tag')).order_by('-post_count')[:10]
        return render(request, 'trending/trending.html', {"categories":top_10_categories})