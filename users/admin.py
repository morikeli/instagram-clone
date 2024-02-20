from django.contrib import admin
from .models import Post, LikedPost, Comment, Friend


@admin.register(Post)
class UsersPostsTable(admin.ModelAdmin):
    list_display = ['user', 'total_likes', 'date_posted']


@admin.register(LikedPost)
class LikedPostsTable(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_created']


@admin.register(Comment)
class CommentsTable(admin.ModelAdmin):
    list_display = ['name', 'comment']


@admin.register(Friend)
class FriendsTable(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created']