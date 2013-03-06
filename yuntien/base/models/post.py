import datetime
from django.db import models
from django.contrib.auth.models import User
from yuntien.base.models.tag import *
from yuntien.base.settings import *
from yuntien.util.url import get_domain, transform_video_url
from yuntien.authext.models.auth import AuthEntMixin

TYPE_NORMAL = 0
TYPE_HAS_VIDEO = 1
TYPE_HAS_IMAGE = 2
TYPE_INVALID = 999

class PostBase(AuthEntMixin, TagEntMixin, models.Model):
    
    class Meta:
        abstract = True
        ordering = ['-date_time']
        get_latest_by = "date_time"

    author = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_set")
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    raw_content = models.TextField(blank=True)
    
    link = models.URLField(blank=True)

    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    type = models.IntegerField(default=0)
  
    hot = models.BooleanField(default=False)
    
    @property
    def has_video(self):
        has_video, video_link = transform_video_url(self.link)
        return has_video

    @property
    def video_link(self):
        has_video, video_link = transform_video_url(self.link)
        return video_link
    
    @property
    def has_image(self):
        return self.type == TYPE_HAS_IMAGE    

    def __unicode__(self):
        return self.title

    def get_owner_id(self):
        return self.author_id

    def is_valid(self):
        return self.type != TYPE_INVALID
