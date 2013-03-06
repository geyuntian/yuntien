from django.db import models
from django.contrib.auth.models import User
from yuntien.authext.models.user import *

TYPE_DEFAULT = 0
TYPE_MINOR = 1

class RevisionMixin(object):
    @classmethod
    def add_version(cls, obj):
        last = cls.all().ancestor(obj).order('-version').get()
        #we need transaction support for revision
        new = cls(parent=obj)
        if last:
            new.version = last.version + 1
        return new        

class RevisionEntMixin(object):
    @classmethod
    def get_revision_class(cls):
        return YTRevision

    @classmethod
    def use_revision(cls):
        return True
        
    def add_version(self):
        return self.get_revision_class().add_version(self)
    
class RevisionBase(RevisionMixin, models.Model):
    
    class Meta:
        abstract = True    
    
    version = models.IntegerField(default=1)
    type = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_set")
    comment = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    
class TextRevisonBase(RevisionBase):

    class Meta:
        abstract = True    
    
    content = models.TextField(blank=True)
    raw_content = models.TextField(blank=True)

