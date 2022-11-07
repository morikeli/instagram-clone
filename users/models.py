from django.db import models
from accounts.models import UserProfile
from PIL import Image


class Posts(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=True)
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

    def save(self, *args, **kwargs):
        super(Posts, self).save(*args, **kwargs)

        posted_img = Image.open(self.image.path)

        if posted_img.height > 500 and posted_img.width > 500:
            output_size = (500, 500)
            posted_img.thumbnail(output_size)
            posted_img.save(self.image.path)


class LikedPost(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=50, editable=False)
    liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['liked']
    
    def __str__(self):
        return f'{self.username}'
