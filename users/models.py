from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from accounts.models import User
from PIL import Image


def user_directory_path(instance, filename):
    """ Files will be uploaded to MEDIA_ROOT/user_{id}/filename """
    return f'user_{str(instance.user.id)[:5]}/posts/{filename}'


class Tag(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
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
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
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
    post = models.ForeignKey('Post', on_delete=models.CASCADE, editable=False)
    date_posted = models.DateTimeField()  # date of the post posted by user object "following"
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'NewsFeed'
        ordering = ['date_posted']
    
    
    def __str__(self):
        return f'{self.following}'
    

class PostedContentFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='files')
    posted_file = models.FileField(upload_to=user_directory_path)
    date_created = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    caption = models.TextField(blank=True)
    total_likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, editable=False)
    liked_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='liked_post', editable=False)
    tags = models.ManyToManyField(Tag, related_name='tags')
    is_liked = models.BooleanField(default=False, editable=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user}'


    def save_uploaded_files(self, files):
        """ Call this function to save a post when a user uploads file(s). A user can upload one or more files. """
        for f in files:
            PostedContentFiles.objects.create(user=self.user, posted_file=f, post_id=self.id)
    

    def get_posted_images(self):
        """ Returns all the images related to this post. A user can upload more than one image files, therefore, this function
            retrieves all files related to this post.
        """
        return PostedContentFiles.objects.filter(post_id=self.id)


    def get_total_likes(self):
        return self.total_likes.count()


    def get_liked_by_user_profile_pic(self):
        """ Method to get profile pictures of the first three users who liked the post. """
        
        liked_users = self.total_likes.all()[:3]
        profile_pictures = [user.profile_pic for user in liked_users]
        return profile_pictures


    def get_comments(self):
        return Comment.objects.filter(item=self.id)


    def total_comments(self):
        return Comment.objects.filter(item=self.id).count()
    

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-date_posted']


class Comment(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    item = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    comment = models.TextField(blank=False)
    date_commented = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item}"


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        (1, 'Like'),
        (2, 'Comment'),
        (3, 'Follow')
    )

    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', editable=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', editable=False)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    notification_text = models.CharField(max_length=50)     # comment for a given post
    is_read = models.BooleanField(default=False, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.notification_type
