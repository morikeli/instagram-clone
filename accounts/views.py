from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class UserLogin(LoginView):
    template_name = 'accounts/login.html'

def signup_view(request):

    return render(request, 'accounts/signup.html')

class LogoutUser(LogoutView):
    template_name = 'accounts/logout.html'