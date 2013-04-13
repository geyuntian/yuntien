from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from yuntien.base.models.image import ImageMixin
from yuntien.user.settings import DEFAULT_USER_PROFILE_IMAGE
from yuntien.user.models.relation import *
from yuntien.authext.models.user import get_current_user

class User(ImageMixin, AbstractUser):
    class Meta(AbstractUser.Meta):
        app_label = 'user'
        
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    temp_email = models.EmailField(blank=True)

    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    
    has_profile_image = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('user-display', kwargs={'user':self.username})

    @property
    def name(self):
        return self.username

    @property
    def profile_image(self):
        if self.has_profile_image:
            return default_storage.url('icon/user/%d.jpg' % self.id)
        
        return DEFAULT_USER_PROFILE_IMAGE
    
    @property
    def friends(self):
        return [u.user2 for u in self.friend_set.all()[:12]]

    @property
    def followers(self):
        return [u.user1 for u in self.follower_set.all()[:12]]
    
    def create_friendship(self, user):
        if self.id == user.id:
            return
        if self.friends_count >= 100:
            return
        if Relation.create(self, user):
            self.friends_count += 1
            self.save()
            user.followers_count += 1
            user.save()

    #Better to patch the user model?
    def destroy_friendship(self, user):
        if Relation.destroy(self, user):
            self.friends_count -= 1
            self.save()
            user.followers_count -= 1
            user.save()
            
    def is_friend(self, user=None):
        if not user:
            user = get_current_user()        
        return Relation.exists(user, self)
    
    def get_profile(self):
        return self
