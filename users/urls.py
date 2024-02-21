from django.urls import path
from . import views
from . import htmx


urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('profile/<str:user_id>/', views.SuggestedUserProfileView.as_view(), name='view_user_profile'),
    
]

htmx_urlpatterns = [
    path('sugeested-user/follow/', htmx.follow_or_unfollow_users_homepage, name='follow_suggested_user'),
    path('<str:user_id>/follow/', htmx.follow_or_unfollow_users_in_profile_page, name='follow_user'),
    path('like/', htmx.like_or_unlike_post, name='like_or_unlike'),

]

urlpatterns += htmx_urlpatterns
