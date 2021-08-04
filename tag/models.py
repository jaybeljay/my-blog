from django.db import models
from django.urls import reverse

from common.utils import gen_slug


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    
    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})
        
    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})
        
    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
