from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like

@receiver(post_save, sender=Like)
def post_save_like_post(sender, instance, **kwargs):
    user_ = instance.user
    post_ = instance.post
    if kwargs.get('created'):
        post_.liked.add(user_)
        post_.save()

@receiver(post_delete, sender=Like)
def post_save_remove_like(sender, instance, **kwargs):
    user_ = instance.user
    post_ = instance.post
    post_.liked.remove(user_)
    post_.save()