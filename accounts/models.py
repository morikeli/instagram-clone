from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField()
    gender = models.CharField(max_length=7, blank=False)
    country = models.CharField(max_length=30, blank=False)
    phone_no = models.CharField(max_length=14, blank=False)
    profile_pic = models.ImageField(upload_to='User-Dps/', default='default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['username']
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        dp = Image.open(self.profile_pic.path)
        
        if dp.height > 400 and dp.width > 400:
            output_size = (400, 400)
            dp.thumbnail(output_size)
            dp.save(self.profile_pic.path)

