from django.urls import path

from .views import TagCreate, TagUpdate, TagDelete, tags_list, tag_detail

urlpatterns = [
    path('', tags_list, name='tags_list'),
    path('create/', TagCreate.as_view(), name='tag_create_url'),
    path('<slug:slug>/', tag_detail, name='tag_detail_url'),
    path('<slug:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('<slug:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
]
