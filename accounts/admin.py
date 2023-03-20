from django.contrib import admin
from .models import User
from .forms import SignUpForm
from django.contrib.auth.admin import UserAdmin

class UserLayout(UserAdmin):
    model = User
    add_form = SignUpForm
    list_display = ['username', 'email', 'gender', 'date_joined', 'is_staff']

admin.site.register(User, UserLayout)