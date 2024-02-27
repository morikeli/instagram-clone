from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views import View
from .forms import SignUpForm, EditProfileForm
from .models import User
from users.models import Post, Friend, SavedPost


class UserLogin(LoginView):
    template_name = 'accounts/login.html'


class SignupView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {'SignupForm': form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully!')
            return redirect('login')

        context = {'SignupForm': form}
        return render(request, self.template_name, context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False)
def edit_profile_view(request):
    form = EditProfileForm(instance=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated successfully!')
            return redirect('user_profile')

    context = {'edit_form': form}
    return render(request, 'accounts/edit-profile.html', context)


@login_required(login_url='user_login')
@user_passes_test(lambda user: user.is_staff is False)
def profile_view(request):
    user_following = Friend.objects.filter(follower=request.user).count()
    total_followers = Friend.objects.filter(following=request.user).count()
    total_posts = Post.objects.filter(user=request.user).count()
    user_posts = Post.objects.filter(user=request.user)
    _followers = Friend.objects.filter(following=request.user)
    _following = Friend.objects.filter(follower=request.user)
    saved_posts = SavedPost.objects.filter(user=request.user, is_saved=True)

    
    context = {
        'my_posts': user_posts,
        'total_posts': total_posts,
        'following': user_following, 
        'followers': total_followers,
        'my_followers': _followers,
        'people_i_follow': _following,
        'saved_posts': saved_posts,
    }
    return render(request, 'accounts/profile.html', context)


class LogoutUser(LogoutView):
    template_name = 'accounts/login.html'
