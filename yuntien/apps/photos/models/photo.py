from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from yuntien.authext.models.auth import AuthEntMixin, AuthCheckParent
from yuntien.user.models import Widget as UserWidget
from yuntien.community.main.models import Community
from yuntien.community.main.models import Widget as CommunityWidget
from yuntien.community.common.models import Text
from yuntien.base.models.image import *
from yuntien.framework.models.source import SourceMixin
from yuntien.app.models.app import App
from yuntien.status.models.status import *

class Photo(AuthEntMixin, ImageMixin, SourceMixin, models.Model):
    
    class Meta:
        app_label = 'photos'
        ordering = ['-date_time']

    user = models.ForeignKey(User, blank=True, null=True)
    
    type = models.IntegerField(default=0)
    
    date_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=140)

    status = models.ForeignKey(Status, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)

    def __unicode__(self):
        return '%s' %(self.title)
    
    def save(self, *args, **kwargs):
        add_status = not self.id
        super(Photo, self).save(*args, **kwargs) 
        if add_status:        
            s = Status()
            s.user = self.user
            s.app = self.source_widget.app
            s.source_type = self.source_type
            s.source_id = self.source_id
            s.source_widget_id = self.source_widget_id
            
            s.content_type = ContentType.objects.get_for_model(Photo)
            s.object_id = self.id
            s.title = self.title
            s.save()
            self.status = s
            super(Photo, self).save(*args, **kwargs)
            
    def delete(self):
        try:
            self.status.delete()
        except:
            pass

        default_storage.delete(self.thumbnail_name)
        default_storage.delete(self.large_name)
        default_storage.delete(self.medium_name)

        super(Photo, self).delete()

    @property
    def thumbnail_name(self):
        return u'thumbnail/photos/%d.jpg' % self.id
    
    @property
    def thumbnail_url(self):
        return default_storage.url(u'thumbnail/photos/%d.jpg' % self.id)
    
    @property
    def large_name(self):
        return u'large/photos/%d.jpg' % self.id

    @property
    def large_url(self):
        return default_storage.url(u'large/photos/%d.jpg' % self.id)

    @property
    def medium_name(self):
        return u'medium/photos/%d.jpg' % self.id        
    
    @property
    def medium_url(self):
        return default_storage.url(u'medium/photos/%d.jpg' % self.id)        
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.source
