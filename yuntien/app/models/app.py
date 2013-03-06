from django.db import models
from django.contrib.auth.models import User
from yuntien.base.models.tag import TagBase, TagEntMixin
from yuntien.app.settings import APPS

class Tag(TagBase):

    class Meta(TagBase.Meta):
        app_label = 'app'

class App(TagEntMixin, models.Model):
    
    class Meta:
        app_label = 'app'
        ordering = ['-sort']
    
    key_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)

    count = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User)
    style = models.IntegerField(default=0) #0:wide
    type = models.IntegerField(default=0) #0:internal, 1:external
    
    multiple_widgets = models.BooleanField(default=True) #default true now
    has_app_page = models.BooleanField(default=True)
    
    supports_community = models.BooleanField(default=True)
    supports_user = models.BooleanField(default=True)
    
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_tag_class(cls):
        return Tag
    
    @property
    def settings(self):
        return APPS[self.key_name]
    
    @property
    def render_status(self):
        if 'render_status' in self.settings:
            return self.settings['render_status']
        return False
    
    def save(self, *args, **kwargs):
        super(App, self).save(*args, **kwargs)
        self.add_tags_to_db()
        super(App, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        Tag.remove_tags([tag.name for tag in self.tags.all()])
        super(App, self).delete(*args, **kwargs)
