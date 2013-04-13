import urllib, hashlib
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from yuntien.base.models.image import ImageMixin
from yuntien.user.settings import DEFAULT_USER_PROFILE_IMAGE
from yuntien.user.models.relation import *
from yuntien.authext.models.user import get_current_user

class UserProfile(ImageMixin, models.Model):
    
    class Meta:
        app_label = 'user'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    email = models.EmailField(blank=True)
    
    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    
    has_profile_image = models.BooleanField(default=False)
    
    @property
    def profile_image(self):
        if self.has_profile_image:
            return default_storage.url('icon/user/%d.jpg' % self.user_id)
        
        return DEFAULT_USER_PROFILE_IMAGE
    
    @property
    def friends(self):
        return [u.user2 for u in self.user.friend_set.all()[:12]]

    @property
    def followers(self):
        return [u.user1 for u in self.user.follower_set.all()[:12]]
    
    #Better to patch the user model?
    def create_friendship(self, user):
        if self.user.id == user.id:
            return
        if self.friends_count >= 100:
            return
        if Relation.create(self.user, user):
            self.friends_count += 1
            self.save()
            p = user.get_profile()
            p.followers_count += 1
            p.save()

    #Better to patch the user model?
    def destroy_friendship(self, user):
        if Relation.destroy(self.user, user):
            self.friends_count -= 1
            self.save()
            p = user.get_profile()
            p.followers_count -= 1
            p.save()
            
    def is_friend(self, user=None):
        if not user:
            user = get_current_user()        
        return Relation.exists(user, self.user)
    
def _create_profile(sender, **kwargs):
    if kwargs.get('created', None):
        u = UserProfile(user=kwargs.get('instance'))
        u.save()
        
#post_save.connect(_create_profile, sender=get_user_model())
