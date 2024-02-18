from django.urls import path
from . import views
from . import validators

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('create-account/', views.SignupView.as_view(), name='signup'),
    path('profile', views.profile_view, name='user_profile'),
    path('edit/', views.edit_profile_view, name='edit_profile'),

    path('logout/', views.LogoutUser.as_view(), name='logout'),    
]

htmx_urlpatterns = [
    path('validate-username/', validators.check_username_exists, name='validate_username'),
    path('validate-email/', validators.email_address_validation, name='validate_email'),
    path('validate-mobile/', validators.mobile_number_validation, name='validate_mobile_number'),
    path('check-password/', validators.password_match_and_length_validation, name='check_password'),
]

urlpatterns += htmx_urlpatterns