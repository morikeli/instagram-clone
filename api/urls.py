from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup', views.SignupAPIView.as_view()),
]