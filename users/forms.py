from django import forms
from .models import Post, Comment

class CreatePostsForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type caption ...'}))
    class Meta:
        model = Post
        fields = ['image', 'caption']
