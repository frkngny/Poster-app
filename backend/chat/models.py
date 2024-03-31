from django.db import models
from account.models import User
import uuid
from django.utils import timezone
from django.utils.timesince import timesince


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)
    
    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def __str__(self) -> str:
        threshold_len = 20
        ex = ""
        if len(self.body) > threshold_len:
            ex = "..."
        return self.body[0:threshold_len] + ex
    
    class Meta:
        ordering = ['created_at']
