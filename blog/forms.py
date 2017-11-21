from django import forms
from .models import Post

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("author", "title", "content", "image")
        
class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")