from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posts

@login_required(login_url='user_login')
def homepage_view(request):
    posted_posts = Posts.objects.all()

    context = {'posted': posted_posts}
    return render(request, 'users/homepage.html', context)