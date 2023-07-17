from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class follower(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + " followed " + self.followee.username
