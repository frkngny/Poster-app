from django.db import models
import uuid 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from account.models import User
from django.utils.timesince import timesince


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    liked = models.ManyToManyField(User, blank=True, related_name='likes')
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
        
    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def likes_count(self):
        return self.liked.all().count()
    

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)