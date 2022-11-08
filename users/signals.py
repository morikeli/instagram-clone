from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import UserProfile
from .models import Posts
import uuid

@receiver(pre_save, sender=Posts)
def generate_posts_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:15]

