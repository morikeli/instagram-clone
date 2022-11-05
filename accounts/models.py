from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    name = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    bio = models.TextField()
    gender = models.CharField(max_length=7, blank=False)
    country = models.CharField(max_length=30, blank=False)
    phone_no = models.CharField(max_length=14, blank=False)
    profile_pic = models.ImageField(upload_to='User-Dps/', default='default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Users Profile'

    def __str__(self):
        return f'{self.name.username}'