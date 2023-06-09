from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from accounts.models import Notification
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Notification
from django.urls import reverse
from django.utils.html import format_html
from mountains.models import Mountain

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True,null=True)
    mountain = models.ForeignKey(Mountain, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')


class PostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_postcomments')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_postcomments')
    
    def save(self, *args, **kwargs):
        created = not self.pk  
        super().save(*args, **kwargs)
        if created and self.user != self.post.user:
            recipient = self.post.user 
            post_url = reverse('posts:detail', kwargs={'post_pk': self.post.pk})  
            message = f'{self.user.username}님이 <a href="{post_url}">{self.post.title}</a> 게시물에 댓글을 남겼습니다.'
            notification = Notification.objects.create(user=recipient, notification_type='댓글', message=message)
            
