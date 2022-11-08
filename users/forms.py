from django import forms
from .models import Posts, Comments

class CreatePostsForm(forms.ModelForm):
    
    class Meta:
        model = Posts
        fields = ['image']
