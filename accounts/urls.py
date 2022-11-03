from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('create-account/', views.signup_view, name='signup'),
    path('logged-out/', views.LogoutUser.as_view(), name='logout_user'),    
]
