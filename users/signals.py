from .models import Post, Comment, Friend, Tag, NewsFeed, Notification
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import uuid


@receiver(pre_save, sender=Post)
def generate_posts_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=Comment)
def generate_comments_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=Friend)
def generate_followers_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=Tag)
def generate_tags_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=NewsFeed)
def generate_news_feed_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=Notification)
def generate_notification_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(post_save, sender=Post)
def add_post(sender, instance, created, *args, **kwargs):
    """ This signal updates the current user's followers news feed when he/she posts something. """
    
    if created:
        post = instance
        user = post.user
        followers = Friend.objects.filter(following=user)    # filter users following the current user

        for follower in followers:
            user_feed = NewsFeed.objects.get_or_create(
                post=post,
                user=user,
                date_posted=post.date_posted,
                following=follower.follower,
            )

