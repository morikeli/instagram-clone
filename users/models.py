from django.db import models
from accounts.models import UserProfile

class Posts(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to='UserPosts/', null=False)
    caption = models.TextField(blank=True)
    total_likes = models.PositiveIntegerField(default=0, editable=False)
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['user']

class LikedPost(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=50, editable=False)
    liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['liked']
    
    def __str__(self):
        return f'{self.username}'
