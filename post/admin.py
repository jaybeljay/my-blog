from django.contrib import admin
from .models import UpvoteDownvote, Post, Comment


class UpvoteDownvoteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UpvoteDownvote._meta.fields]
    
    class Meta:
        model = UpvoteDownvote
    

admin.site.register(UpvoteDownvote, UpvoteDownvoteAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]
    
    class Meta:
        model = Post
    

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    
    class Meta:
        model = Comment
    
admin.site.register(Comment, CommentAdmin)
