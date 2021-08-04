from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Tag
from .forms import TagForm
from common.utils import StaffCheckMixin


class TagCreate(StaffCheckMixin, View):
    def get(self, request):
        form = TagForm()
        return render(request, 'tag_create.html', {'form': form})
        
    def post(self, request):
        bound_form = TagForm(request.POST)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'tag_create.html', {'form': bound_form})
        

class TagUpdate(StaffCheckMixin, View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        bound_form = TagForm(instance=tag)
        return render(request, 'tag_update.html', {'form': bound_form, 'tag': tag})
        
    def post(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        bound_form = TagForm(request.POST, instance=tag)
        
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'tag_update.html', {'form': bound_form, 'tag': tag})
        

class TagDelete(StaffCheckMixin, View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        return render(request, 'tag_delete.html', {'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        tag.delete()
        return redirect(reverse('tags_list'))
        

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags_list.html', {'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug=slug)
    return render(request, 'tag_detail.html', {'tag': tag, 'detail': True, 'admin_tag': tag})
