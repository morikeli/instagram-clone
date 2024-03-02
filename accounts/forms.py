from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User
from .utils import is_image_file


class UserLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.error_messages['invalid_login'] = 'INVALID CREDENTIALS!!! Username and password maybe case-sensitive'


class SignUpForm(UserCreationForm):
    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Username', 'class': 'mb-2', 'autofocus': 'on', 'autocomplete': 'off'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Email', 'class': 'mb-2'}), required=True)
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Enter your mobile no.', 'class': 'mb-2'}), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


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
    profile_pic = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control mb-2', 'accept': '.jpg, .jpeg, .png',
        }),
        required=False,
        validators=[is_image_file],
    )

    class Meta:
        model = User
        fields = ['profile_pic', 'bio', 'phone_no', 'gender', 'country']
