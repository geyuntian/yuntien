from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User
from yuntien.authext.models.ra import RABase, RAEntMixin
from yuntien.authext.models.auth import AuthEntMixin, AuthWithRA, ROLE_USER, ROLE_OWNER
from yuntien.authext.models import auth
from yuntien.authext.models.user import get_current_user
from yuntien.base.models.tag import TagBase, TagEntMixin
from yuntien.app.models.app import App
from yuntien.base.models.image import ImageMixin
from yuntien.framework.models import widget
from yuntien.community.main.settings import APPS
from yuntien.community.main.settings import DEFAULT_COMMUNITY_LOGO

LATEST_MEMBERS_NUM = 20
STYLE_SIMPLE = 0
STYLE_TAB = 1

class Tag(TagBase):

    class Meta(TagBase.Meta):
        app_label = 'main'

class Community(AuthEntMixin, RAEntMixin, TagEntMixin, ImageMixin, models.Model):
    
    class Meta:
        app_label = 'main'
        ordering = ['-sort']
    
    key_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)

    count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User)
    style = models.IntegerField(default=0)
    area_count = models.IntegerField(default=0)
    widget_count = models.IntegerField(default=0)
    
    has_logo_image = models.BooleanField(default=False)
    
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_tag_class(cls):
        return Tag
    
    @classmethod
    def get_auth_class(cls):
        return AuthWithRA
    
    @property
    def logo(self):
        if self.has_logo_image:
            return default_storage.url('icon/community/%d.jpg' % self.id)
        return DEFAULT_COMMUNITY_LOGO
    
    def get_role(self, user):
        if user:
            try:
                return self.ra_set.get(user=user).role
            except:
                pass
    
    def has_joined(self, user=None):
        if not user:
            user = get_current_user()
        if self.get_role(user):
            return True
        return False

    def join(self, user):
        if self.has_joined(user):
            return
        
        self.ra_set.get_or_create(role=ROLE_USER, user=user)
        self.count += 1
        
        self.save()

    def leave(self, user):
        if not self.has_joined(user):# or YTUser.get_current_user().user_id in self.admins:
            return
        
        #creator can't leave
        if self.created_by and self.created_by.id == user.id:
            return
        
        self.ra_set.get(user=user).delete()
        self.count -= 1

        self.save()    
        
    @property
    def latest_members(self):
        return [ra.user for ra in self.ra_set.all()[:LATEST_MEMBERS_NUM]]
    
    def set_admins(self, usernames):
        self.ra_set.filter(user__username__in=usernames).update(role=ROLE_OWNER)
            
    def get_admins(self):
        return [ra.user for ra in self.ra_set.filter(role=ROLE_OWNER)]
    
    def save(self, *args, **kwargs):
        super(Community, self).save(*args, **kwargs)
        self.add_tags_to_db()
        super(Community, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        Tag.remove_tags([tag.name for tag in self.tags.all()])
        super(Community, self).delete(*args, **kwargs)    

class Area(models.Model):
    
    class Meta:
        app_label = 'main'
        ordering = ['-sort']
        unique_together = (("community", "key_name"),)
        
    community = models.ForeignKey(Community)
    key_name = models.CharField(max_length=30)
        
    name = models.CharField(max_length=30)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    widget_count = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' %(self.community.name, self.name)
        
class Widget(RAEntMixin, AuthEntMixin, widget.WidgetBase):
    
    class Meta:
        app_label = 'main'
        ordering = ['-sort']
        unique_together = (("community", "key_name"),)

    community = models.ForeignKey(Community)
    key_name = models.CharField(max_length=30)
    area = models.ForeignKey(Area)
    app = models.ForeignKey(App, related_name="%(app_label)s_%(class)s_set")
    
    name = models.CharField(max_length=30)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)

    num_on_homepage = models.IntegerField(default=10)
    num_per_page = models.IntegerField(default=10)
    
    @property
    def app_config(self):
        return APPS.get(self.app.key_name, None)

    def __unicode__(self):
        return '%s - %s' %(self.community.name, self.name)
    
    @classmethod
    def get_auth_class(cls):
        return auth.AuthCheckParentWithRA 
    
    def get_role(self, user):
        if self.privacy_type == widget.PUBLIC:
            return auth.ROLE_USER
        elif self.privacy_type == widget.MEMBER_ONLY:
            return self.community.get_role(user)
        elif self.privacy_type == widget.OWNER_ONLY:
            role = self.community.get_role(user)
            if role == auth.ROLE_OWNER:
                return auth.ROLE_OWNER
            else:
                return auth.ROLE_GUEST

class RA(RABase):
    
    class Meta(RABase.Meta):
        app_label = 'main'
        
    obj = models.ForeignKey(Community)
    role = models.CharField(max_length=30)    

    def __unicode__(self):
        return '%s - %s' %(self.obj.name, self.user.username)
