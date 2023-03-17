from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage_view, name='homepage'),
    path('profile/<str:suggested_user>/', views.suggested_user_profile_view, name='follow_user_profile'),
    path('like-post/', views.like_posts_view, name='like_post'),
    path('delete-post/', views.delete_posts_view, name='delete_post'),
    
]