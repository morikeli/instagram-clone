from django.contrib import admin
from .models import Posts, LikedPost

@admin.register(Posts)
class UsersPostsTable(admin.ModelAdmin):
    list_display = ['user', 'total_likes', 'posted']

@admin.register(LikedPost)
class LikedPostsTable(admin.ModelAdmin):
    list_display = ['username', 'liked']