from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


def user_directory_path(instance, filename):
    """ Files will be uploaded to MEDIA_ROOT/user_{id}/blogs/filename """
    return f'user_{str(instance.id)[:8]}/profile-pics/{filename}'


class User(AbstractUser):
    id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField()
    gender = models.CharField(max_length=7, blank=False)
    country = models.CharField(max_length=30, blank=False)
    phone_no = PhoneNumberField(blank=False)
    profile_pic = models.ImageField(upload_to=user_directory_path, default='default.png')
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['username']
        verbose_name_plural = 'Users Profile'

    def __str__(self):
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        dp = Image.open(self.profile_pic.path)
        
        if dp.height > 400 and dp.width > 400:
            output_size = (400, 400)
            dp.thumbnail(output_size)
            dp.save(self.profile_pic.path)

