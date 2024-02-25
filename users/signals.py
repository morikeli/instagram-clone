from .models import Post, Comment, Friend, Tag, NewsFeed, Notification
from django.db.models.signals import pre_save, post_save, post_delete
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
def add_post(sender, instance, created, **kwargs):
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


@receiver(post_save, sender=Friend)
def send_follow_notification(sender, instance, created, **kwargs):
    if created:
        follow = instance
        sender = follow.follower
        following = follow.following

        _notify = Notification.objects.get_or_create(sender=sender, receiver=following, notification_type=3)
        _notify


@receiver(post_delete, sender=Friend)
def delete_follow_notification(sender, instance, **kwargs):
    follow = instance
    sender = follow.follower
    following = follow.following

    _notify = Notification.objects.filter(sender=sender, receiver=following, notification_type=3)
    _notify.delete()

