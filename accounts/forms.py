from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class UserLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.error_messages['invalid_login'] = 'INVALID CREDENTIALS!!! Username and password maybe case-sensitive'

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Full Name', 'class': 'mb-2'}), label='', required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Username', 'class': 'mb-2'}), label='', required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Email', 'class': 'mb-2'}), label='', required=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'username', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    bio = forms.CharField(widget=forms.Textarea(attrs={'type': 'text'}), required=False)
    gender = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select', 'class': 'mb-2'}), choices=SELECT_GENDER)
    country = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'mb-2'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'mb-2'}))

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'phone_no', 'gender', 'country']
