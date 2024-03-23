from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Friendship

@receiver(post_save, sender=Friendship)
def post_save_add_to_friends(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    status_ = instance.status
    if status_ == 'accepted':
        sender_.friends.add(receiver_)
        receiver_.friends.add(sender_)
        sender_.save()
        receiver_.save()