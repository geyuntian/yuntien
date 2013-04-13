from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from yuntien.user.models import Widget as UserWidget
from yuntien.community.main.models import Community
from yuntien.community.main.models import Widget as CommunityWidget
from yuntien.framework.models.source import SourceMixin
from yuntien.app.models.app import App

PUBLIC = 0
PROTECTED = 1
PRIVATE = 2

SOURCE_TYPE_DEFAULT = 1
SOURCE_TYPE_USER = 2
SOURCE_TYPE_COMMUNITY = 3

TYPE_DEFAULT = 0
TYPE_IMAGE = 1
TYPE_VIDEO = 2

class Status(SourceMixin, models.Model):
    
    class Meta:
        app_label = 'status'
        ordering = ['-date_time']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    privacy_type = models.IntegerField(default=PUBLIC)
    
    app = models.ForeignKey(App, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)

    is_repost = models.BooleanField(default=False)    
    category = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    
    re_status = models.ForeignKey('self', related_name="re_set", blank=True, null=True, on_delete=models.SET_NULL)
    direct_re_status = models.ForeignKey('self', related_name="direct_re_set", blank=True, null=True, on_delete=models.SET_NULL)
    
    re_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    date_time = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=140)
    
    def __unicode__(self):
        return '%s' %(self.title)
    
    @property
    def has_image(self):
        if self.type == TYPE_IMAGE:
            return True
        return False

    @property
    def user_widget(self):
        if self.source_type == SOURCE_TYPE_USER:
            return UserWidget.objects.get(pk=self.source_widget_id)

    @property
    def community(self):
        if self.source_type == SOURCE_TYPE_COMMUNITY:
            return Community.objects.get(pk=self.source_id)

    @property
    def community_widget(self):
        if self.source_type == SOURCE_TYPE_COMMUNITY:
            return CommunityWidget.objects.get(pk=self.source_widget_id)
        
    @property
    def object(self):
        m = self.content_type.model_class()
        return m.objects.get(pk=self.object_id)

    def set_status(self, status):
        pass
    
    def get_status(self):
        pass
    
    def render(self):
        pass
    
    def delete(self):
        try:
            self.user.statuses_count -= 1
            self.user.save()
            self.community.statuses_count -= 1
            self.community.save()
        except:
            pass
        super(Status, self).delete()
            
    def save(self, *args, **kwargs):   
        add_status = not self.id
        
        if self.source_type == SOURCE_TYPE_DEFAULT:
            self.source_id = self.user.id
        
        super(Status, self).save(*args, **kwargs) 
        if add_status: 
            try:
                self.user.statuses_count += 1
                self.user.save()
                self.community.statuses_count += 1
                self.community.save()
            except:
                pass
            
    def hide(self):
        pass
            
    def repost(self, user, title):
        s = Status()
        s.user = user
#        s.app = self.app
        
        s.category = self.category
        s.type = self.type
        
        s.direct_re_status = self
        if self.is_repost:
            s.re_status = self.re_status
            
            #this status may have been deleted
            try:
                s.re_status.re_count += 1
                s.re_status.save()
            except:
                pass
            
        else:
            s.re_status = self
        
        s.title = title
        s.is_repost = True
        s.save()
        
        self.re_count += 1
        self.save()
        
        return s
