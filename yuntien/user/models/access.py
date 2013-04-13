from django.conf import settings
from django.db import models

class Access(models.Model):
    
    class Meta:
        app_label = 'user'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    
    last_post = models.DateTimeField(auto_now=True)    
    last_day_post = models.IntegerField(default=0)
    last_hour_post = models.IntegerField(default=0)
    last_minute_post = models.IntegerField(default=0)
    
    @classmethod
    def post(cls, user):
        pass
