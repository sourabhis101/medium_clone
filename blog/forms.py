from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image','published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
