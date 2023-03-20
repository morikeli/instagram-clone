from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User
import uuid

@receiver(pre_save, sender=User)
def generate_user_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:20]

