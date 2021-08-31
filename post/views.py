import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import HttpResponse
from django.views import View

from .models import Post, UpvoteDownvote, Comment
from .forms import PostForm, CreateComment
from .services import perform_paginaion, get_top_post, get_all_comments, get_comments_on_the_post, filter_func, create_comment
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
    top_post = get_top_post()
    comments = get_all_comments()
    pages = perform_paginaion(request.GET.get('page', 1), posts)
        
    context = {
        'posts': posts,
        'top_post': top_post,
        'is_paginated': pages['is_paginated'],
        'prev_url': pages['prev_url'],
        'next_url': pages['next_url'],
        'comments': comments,
    }
        
    return render(request, 'posts_list.html', context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_votes = post.votes.rating()
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    comments = get_comments_on_the_post(post)
    
    context = {
        'post': post,
        'post_votes': post_votes,
        'comments': comments,
        'detail': True,
        'admin_post': post
    }
    
    return render(request, 'post.html', context)
   

def filter_search(request):
    result = filter_func(request)
    return render(request, 'search.html', {'queryset': result['posts'], 'tags': result['tags']})


class Voting(LoginRequiredMixin, View):
    model = None
    vote_type = None
    
    def post(self, request, slug):
        obj = self.model.objects.get(slug=slug)
        
        try:
            vote_object = UpvoteDownvote.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if vote_object.vote is not self.vote_type:
                vote_object.vote = self.vote_type
                vote_object.save(update_fields=['vote'])
            else:
                vote_object.delete()
        except UpvoteDownvote.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
        
        return HttpResponse(
            json.dumps({
                'rating': obj.votes.rating()
            }),
            content_type='application/json'
        )


class CommentCreate(View):
    def post(self, request, slug):
        form = CreateComment(request.POST or None)
        if form.is_valid():
            post = Post.objects.get(slug=slug)
            create_comment(request.user, post, request.POST['comment_text'])
            comment_list = Comment.objects.filter(post=post)
            return HttpResponse(render(request, 'comment_section.html', {'comment_list': comment_list}))
        else:
            return HttpResponse('Oops! An error occurred.')
