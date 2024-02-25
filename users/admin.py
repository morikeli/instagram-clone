from django.contrib import admin
from .models import Post, Comment, Friend


@admin.register(Post)
class UsersPostsTable(admin.ModelAdmin):
    list_display = ['user', 'date_posted']


@admin.register(Comment)
class CommentsTable(admin.ModelAdmin):
    list_display = ['item', 'comment']


@admin.register(Friend)
class FriendsTable(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created']