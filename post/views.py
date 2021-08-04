import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator

from .models import UpvoteDownvote, Post, Comment
from .forms import PostForm, CreateComment
from tag.models import Tag
from common.utils import StaffCheckMixin

from hitcount.models import HitCount
from hitcount.views import HitCountMixin


class PostCreate(StaffCheckMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'post_create.html', {'form': form})
        
    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'post_create.html', {'form': bound_form})


class PostUpdate(StaffCheckMixin, View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        bound_form = PostForm(instance=post)
        return render(request, 'post_update.html', {'form': bound_form, 'post': post})
        
    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        bound_form = PostForm(request.POST, instance=post)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'post_update.html', {'form': bound_form, 'post': post})
        

class PostDelete(StaffCheckMixin, View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, 'post_delete.html', {'post': post})
        
    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return redirect(reverse('posts_list'))


def posts_list(request):
    posts = Post.objects.all()
    try:
        top_post = Post.is_new_objects.is_new().order_by('-hit_count_generic__hits')[0] # is_new_objects instead of objects
    except IndexError:
        top_post = None
    paginator = Paginator(posts, 6)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    
    is_paginated = page.has_other_pages()
    
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
        
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
        
    try:
        comments = Comment.objects.all()
    except Comment.DoesNotExist:
        comments = None
        
    context = {
        'posts': page,
        'top_post': top_post,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'comments': comments,
    }
        
    return render(request, 'posts_list.html', context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_votes = post.votes.rating()
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    try:
        comments = Comment.objects.filter(post=post)
    except Comment.DoesNotExist:
        comments = None

    context = {
        'post': post,
        'post_votes': post_votes,
        'comments': comments,
        'detail': True,
        'admin_post': post
    }
    
    return render(request, 'post.html', context)
   

def filter_search(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    text_contains = request.GET.get('text_contains')
    text_exact = request.GET.get('text_exact')
    view_count_min = request.GET.get('min_view')
    view_count_max = request.GET.get('max_view')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    tag = request.GET.get('tag')
    
    def is_valid_param(param):
        return param != '' and param is not None
    
    if is_valid_param(text_contains):
        posts = posts.filter(Q(text__icontains=text_contains) | Q(title__icontains=text_contains) | Q(intro__icontains=text_contains)).distinct()
        
    elif is_valid_param(text_exact):
        posts = posts.filter(Q(text__iexact=text_exact) | Q(title__iexact=text_exact) | Q(intro__iexact=text_exact)).distinct()
        
    if is_valid_param(view_count_min):
        posts = posts.filter(views__gte=view_count_min)
        
    if is_valid_param(view_count_max):
        posts = posts.filter(views__lt=view_count_max) 
        
    if is_valid_param(date_min):
        posts = posts.filter(pub_date__gte=date_min)
        
    if is_valid_param(date_max):
        posts = posts.filter(pub_date__lt=date_max)
        
    if is_valid_param(tag) and tag != 'Choose...':
        posts = posts.filter(tags__title=tag)
    
    return render(request, 'search.html', {'queryset': posts, 'tags': tags})


class Voting(LoginRequiredMixin, View):
    model = None # Post or Comment
    vote_type = None # Upvote or Downvote
    
    def post(self, request, slug):
        obj = self.model.objects.get(slug=slug)
        try:
            vote_object = UpvoteDownvote.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user) # get the voice if it exists
            if vote_object.vote is not self.vote_type: # set the vote_type to the opposite one if the user changed their mind
                vote_object.vote = self.vote_type
                vote_object.save(update_fields=['vote'])
                result = True
            else:
                vote_object.delete()
                result = False
        except UpvoteDownvote.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
        
        return HttpResponse(
            json.dumps({
                'result': result,
                'rating': obj.votes.rating()
            }),
            content_type='application/json'
        )
        

class CommentCreate(View):
    def post(self, request, slug):
        form = CreateComment(request.POST or None)
        if form.is_valid():
            post = Post.objects.get(slug=slug)
            user = User.objects.get(username=request.user)
            comment_text = request.POST.get('comment_text')
            comment = Comment.objects.create(post=post, author_name=user, comment_text=comment_text)
            comment_list = Comment.objects.filter(post=post)
            return HttpResponse(render(request, 'comment_section.html', {'comment_list': comment_list}))
        else:
            return HttpResponse('Oops! An error occurred.')
