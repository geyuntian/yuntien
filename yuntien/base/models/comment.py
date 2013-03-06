from django.db import models
from django.contrib.auth.models import User
from yuntien.authext.models.auth import AuthEntMixin

REFS_LENGTH = 10
TYPE_INVALID = 999
DEEP_DEPTH = 100
            
class CommentBase(AuthEntMixin, models.Model):

    class Meta:
        abstract = True    
    
    author = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_set")
    content = models.TextField(blank=True)
    raw_content = models.TextField(blank=True)
    
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    type = models.IntegerField(default=0)

    hot = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content[:30]
    
    def get_owner_id(self):
        return self.author_id
