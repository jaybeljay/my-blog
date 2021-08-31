from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Post, Comment
from tag.models import Tag


def get_top_post():
    try:
        top_post = Post.is_new_objects.is_new().order_by('-hit_count_generic__hits')[0]
    except IndexError:
        top_post = None


def get_all_comments():
    try:
        comments = Comment.objects.all()
    except Comment.DoesNotExist:
        comments = None


def get_comments_on_the_post(post):
    try:
        comments = Comment.objects.filter(post=post)
    except Comment.DoesNotExist:
        comments = None

    
def create_comment(user, post, comment_text):
    user = User.objects.get(username=user)
    comment = Comment.objects.create(post=post, author_name=user, comment_text=comment_text)


def perform_paginaion(page, posts):
    paginator = Paginator(posts, 6)
    page_num = page
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
        
    result = {
      'is_paginated': is_paginated, 
      'prev_url': prev_url, 
      'next_url': next_url
    }

    return result
    
    
def filter_func(request):
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
        posts = posts.filter(hit_count_generic__gte=view_count_min)
        
    if is_valid_param(view_count_max):
        posts = posts.filter(hit_count_generic__lt=view_count_max) 
        
    if is_valid_param(date_min):
        posts = posts.filter(pub_date__gte=date_min)
        
    if is_valid_param(date_max):
        posts = posts.filter(pub_date__lt=date_max)
        
    if is_valid_param(tag) and tag != 'Choose...':
        posts = posts.filter(tags__title=tag)
        
    context = {
        'posts': posts,
        'tags': tags
    }
    
    return context
