from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage_view, name='homepage'),
    path('like-post/', views.like_posts_view, name='like_post'),
    path('delete-post/', views.delete_view, name='delete_post'),
    
]