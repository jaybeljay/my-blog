from django.forms import ModelForm, TextInput, Textarea, SelectMultiple
from django.core.exceptions import ValidationError

from .models import Comment, Post


class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'intro', 'text', 'slug', 'tags']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'slug': TextInput(attrs={'class': 'form-control'}),
            'intro': Textarea(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug']
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug
