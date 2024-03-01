from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message
import uuid


@receiver(pre_save, sender=Message)
def generate_messages_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]
