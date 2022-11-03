from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import UserLoginForm, SignUpForm

class UserLogin(LoginView):
    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'

def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_profile')

    context = {'SignUpForm': form}
    return render(request, 'accounts/signup.html', context)

class LogoutUser(LogoutView):
    template_name = 'accounts/logout.html'