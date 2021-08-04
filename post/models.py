from datetime import datetime, timedelta

from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from hitcount.models import HitCountMixin, HitCount

from common.utils import gen_slug

from tag.models import Tag
        

class UpvoteDownvoteManager(models.Manager):
    use_for_related_fields = True
    
    def posts(self):
        return self.get_queryset().filter(content_type__model='Post')
    
    def upvotes(self):
        return self.get_queryset().filter(vote__gt=0)
    
    def downvotes(self):
        return self.get_queryset().filter(vote__lt=0)
        
    def rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class UpvoteDownvote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    
    VOTES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote')
    )
    
    vote = models.SmallIntegerField(verbose_name='Vote', choices=VOTES)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    objects = UpvoteDownvoteManager()
    
    class Meta:
        verbose_name = 'Upvote and Downvote'
        verbose_name_plural = 'Upvotes and Downvotes'


class PostManager(models.Manager):
    def is_new(self):
        return self.get_queryset().filter(pub_date__gt=(datetime.now() - timedelta(days=7)))


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=200)
    intro = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    votes = GenericRelation(UpvoteDownvote, blank=True, related_query_name='posts')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    objects = models.Manager()
    is_new_objects = PostManager()
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
        
    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})
        
    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    
    def __str__(self):
        return '{}: {}'.format(self.author_name, self.comment_text)
