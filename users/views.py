from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='user_login')
def homepage_view(request):

    context = {}
    return render(request, 'users/homepage.html', context)