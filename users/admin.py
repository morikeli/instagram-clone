from django.contrib import admin
from .models import Posts, LikedPost, Comments

@admin.register(Posts)
class UsersPostsTable(admin.ModelAdmin):
    list_display = ['user', 'total_likes', 'posted']

@admin.register(LikedPost)
class LikedPostsTable(admin.ModelAdmin):
    list_display = ['username', 'liked']


@admin.register(Comments)
class LikedPostsTable(admin.ModelAdmin):
    list_display = ['name', 'comment']