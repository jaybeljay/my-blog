from django.urls import path

from .views import (PostCreate, PostUpdate, PostDelete, 
    posts_list, post, filter_search, Voting, CommentCreate)
from .models import UpvoteDownvote, Post

urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('create/', PostCreate.as_view(), name='post_create_url'),
    path('search/', filter_search, name='filter_search'),
    path('<slug:slug>/', post, name='post_detail'),
    path('<slug:slug>/upvote/', Voting.as_view(model=Post, vote_type=UpvoteDownvote.UPVOTE), name='post_upvote'),
    path('<slug:slug>/downvote/', Voting.as_view(model=Post, vote_type=UpvoteDownvote.DOWNVOTE), name='post_downvote'),
    path('<slug:slug>/comment/', CommentCreate.as_view(), name='comment_create'),
    path('<slug:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
]
