from post.models import post, like
from account.models import Profile
from django.db.models import Subquery, OuterRef, Exists, Count, F

class comment:

    @staticmethod
    def getComments(request, post_id):
        main = post.objects.get(id=post_id);
        comments = post.objects.filter(referenced_post=main).order_by('-time')
        main_post = post.objects.filter(id=post_id)
        comments = main_post | comments

        user_likes = like.objects.filter(user=request.user, post=OuterRef('pk'))
        comments = comments.annotate(user_like=Exists(user_likes))

        # Annotate the 'creator_profile_image' field to get the profile picture of the post creator
        profiles = Profile.objects.filter(user__in=Subquery(comments.values('user')))
        comments = comments.annotate(creator_profile_image=Subquery(profiles.filter(user=OuterRef('user')).values('image')[:1]))

        # Annotate the 'comment_count' field to get the number of comments for each post
        comment_counts = post.objects.filter(referenced_post=OuterRef('pk')).values('pk').annotate(comment_count=Count('pk'))
        comments = comments.annotate(comment_count=Subquery(comment_counts.values('comment_count')))
        return comments
        
    @staticmethod
    def createComment(request):
        post_id = request.POST.get("post_id")
        message = request.POST.get("content")
        Original_post = post.objects.get(id=post_id)
        post.objects.create(user=request.user, text=message, tag=Original_post.tag, referenced_post=Original_post)