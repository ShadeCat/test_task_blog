from django import forms
from testtask.models import Post


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

