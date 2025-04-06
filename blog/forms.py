from django import forms
from .models import ModelPost


class PostForm(forms.ModelForm):
    class Meta:
        model = ModelPost
        fields = ['title', 'content']
