from typing import Any
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text