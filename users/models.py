from django.db import models
from accounts.models import User
from PIL import Image


class Friends(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    following = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    followed = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.following}'

    class Meta:
        verbose_name_plural = 'Followers'


class Posts(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=True)
    image = models.ImageField(upload_to='UserPosts/', null=False)
    caption = models.TextField(blank=True)
    total_likes = models.PositiveIntegerField(default=0, editable=False)
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['posted']

    def save(self, *args, **kwargs):
        super(Posts, self).save(*args, **kwargs)

        posted_img = Image.open(self.image.path)

        if posted_img.height > 500 and posted_img.width > 500:
            output_size = (500, 500)
            posted_img.thumbnail(output_size)
            posted_img.save(self.image.path)

class Comments(models.Model):
    id = models.CharField(max_length=10, primary_key=True, editable=False, unique=False)
    name = models.ForeignKey(Posts, on_delete=models.CASCADE, editable=False)
    comment = models.TextField(blank=False)
    commented = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class LikedPost(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    post_id = models.CharField(max_length=15, blank=False, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['liked']
    
    def __str__(self):
        return f'{self.username}'

