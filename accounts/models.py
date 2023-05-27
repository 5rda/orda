from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, blank=True)
    profile = models.ImageField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    message = models.CharField(max_length=200, blank=True)