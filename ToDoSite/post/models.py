from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
    
class like(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)