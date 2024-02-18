from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from accounts.models import User
from PIL import Image


def user_directory_path(instance, filename):
    """ Files will be uploaded to MEDIA_ROOT/user_{id}/filename """
    return f'user_{instance.user.id}/{filename}'


class Tag(models.Model):
    id = models.CharField(max_length=25, primary_key=True, editable=False)
    title = models.CharField(max_length=25, verbose_name='Tag')
    slug = models.SlugField(null=True, unique=True)


    class Meta:
        verbose_name_plural = 'Tags'


    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Friend(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='follower')   # current logged in user
    following = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='following')  # this user is followed by the current logged in user
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.follower}'


    class Meta:
        verbose_name_plural = 'Followers'


class NewsFeed(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    following = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='following_feed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    post_date = models.DateTimeField()  # date of the post posted by user object "following"


    class Meta:
        verbose_name_plural = 'NewsFeed'
        ordering = ['post_date']
    
    
    def __str__(self):
        return f'{self.following}'
    

class Post(models.Model):
    id = models.CharField(max_length=25, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to=user_directory_path, null=False)
    caption = models.TextField(blank=True)
    total_likes = models.PositiveIntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag, related_name='tags')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'
    

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['date_posted']


    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        posted_img = Image.open(self.image.path)

        if posted_img.height > 500 and posted_img.width > 500:
            output_size = (500, 500)
            posted_img.thumbnail(output_size)
            posted_img.save(self.image.path)


class Comment(models.Model):
    id = models.CharField(max_length=25, primary_key=True, editable=False, unique=False)
    name = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    comment = models.TextField(blank=False)
    commented = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class LikedPost(models.Model):
    id = models.CharField(max_length=25, primary_key=True, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['liked']
    
    def __str__(self):
        return f'{self.user}'

