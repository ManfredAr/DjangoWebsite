from post.models import post, like
from django.http import JsonResponse
    
class userLikes:

    @staticmethod
    def userLike(request):
        '''
        This method updates the like count for a post.
        '''
        if request.method == "POST":
            post_id = request.POST.get("form_id")
            # Gets the post object.
            post_obj = post.objects.get(id=post_id)
            user_like = True;
            button = "like-count-" + post_id
            if (like.objects.filter(post=post_obj, user=request.user).exists()):
                #If the user unlikes a post then delete the row in likes table.
                user_like = False
                like_obj = like.objects.get(post_id=post_id, user_id=request.user.id)
                like_obj.delete()
                post_obj.likes = like.objects.filter(post_id=post_id).count()
                post_obj.save()
            else:
                # If user likes a post then add a row in the likes table.
                like.objects.create(post=post_obj, user=request.user)
                post_obj.likes = like.objects.filter(post_id=post_id).count()
                post_obj.save()

            # Return a JSON response indicating success
            return JsonResponse({'like_count': post_obj.likes, 'user_like': user_like, 'id': button, 'post_id':post_id})

        # Return a JSON response indicating error
        return JsonResponse({'error': 'Invalid request.'}, status=400)