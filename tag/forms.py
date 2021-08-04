from django.forms import ModelForm, TextInput
from django.core.exceptions import ValidationError

from .models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'slug': TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_slug(self):
        new_slug = self.cleaned_data['slug']
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We already have "{}" slug'.format(new_slug))
        return new_slug
