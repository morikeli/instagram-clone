from django.forms import ClearableFileInput
from django import forms
from .models import Post, InstagramStory
from .utils import is_valid_media_file


class CreatePostsForm(forms.ModelForm):
    """ This form allows a user to post photos or videos on his/her news feed. """

    caption = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Type caption ...'
        }),
        required=False,
    )

    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'type': 'file',
            'class': 'form-control mb-2',
            'accept': '.3gpp, .jpg, .jpeg, .mp4, .mpeg, .ogg, .opus, .png, .wav',
            'multiple': True,
        }),
        required=True,
        validators=[is_valid_media_file],   # perform form validations
    )


    class Meta:
        model = Post
        fields = ['caption', 'image']


class PostInstagramStoryForm(forms.ModelForm):
    """ This form is used to upload images in a user's instagram stories """

    caption = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Type caption ...'
        }),
        required=False,
    )

    story = forms.FileField(widget=forms.FileInput(attrs={
            'type': 'file',
            'class': 'form-control mb-2',
            'accept': '.3gpp, .jpg, .jpeg, .mp4, .mpeg, .ogg, .opus, .png, .wav',
        }),
        required=True,
        validators=[is_valid_media_file],   # perform form validations
    )

    class Meta:
        model = InstagramStory
        fields = ['caption', 'story']