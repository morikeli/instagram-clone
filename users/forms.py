from django import forms
from .models import Posts, Comments

class CreatePostsForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type caption ...'}))
    class Meta:
        model = Posts
        fields = ['image', 'caption']
