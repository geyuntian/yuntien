from django.db import models
from django.contrib.auth.models import User
from yuntien.user.models import Widget as UserWidget
from yuntien.community.main.models import Community
from yuntien.community.main.models import Widget as CommunityWidget
from yuntien.community.common.models import Text
from yuntien.app.models.app import App

class Album(models.Model):
    
    class Meta:
        app_label = 'photos'
        ordering = ['-date_time']
