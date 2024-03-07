from django.urls import path
from . import views
from . import htmx


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('profile/<str:user_id>/', views.SuggestedUserProfileView.as_view(), name='view_user_profile'),
    path('explore/', views.ExplorePostsView.as_view(), name='explore'),
    path('search', views.SearchView.as_view(), name='search'),
    path('notifications/', views.UserNotificationsView.as_view(), name='notifications'),
    
]

htmx_urlpatterns = [
    path('suggested-user/follow/', htmx.follow_or_unfollow_users_homepage, name='follow_suggested_user'),
    path('<str:user_id>follow/', htmx.follow_or_unfollow_viewed_user, name='follow_viewed_user'),
    path('follow/', htmx.follow_or_unfollow_users_in_profile_page, name='follow_user'),
    path('post/like/', htmx.like_or_unlike_post, name='like_or_unlike'),
    path('post/delete/', htmx.delete_post, name='delete_post'),
    path('post/save/', htmx.save_favorite_posts, name='save_favorite_post'),
    path('comment/like/', htmx.like_or_unlike_comment, name='like_or_unlike_comment'),
    path('comment/', htmx.add_comment, name='post_comment'),
    path('comment/delete/', htmx.delete_comment, name='delete_comment'),
    path('story/add', htmx.upload_instagram_story, name='upload_story'),

]

urlpatterns += htmx_urlpatterns
