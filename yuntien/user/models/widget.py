from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from yuntien.app.models.app import App
from yuntien.app.settings import APPS
from yuntien.user.models.user import User
from yuntien.user.settings import USER_WIDGETS

class Widget(models.Model):
    
    class Meta:
        app_label = 'user'
        ordering = ['-sort']
        unique_together = (("user", "key_name"),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_set")
    key_name = models.CharField(max_length=30)
#    area = models.ForeignKey(Area)
    app = models.ForeignKey(App, related_name="%(app_label)s_%(class)s_set")
    
    name = models.CharField(max_length=30)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    @property
    def app_config(self):
        return APPS.get(self.app.key_name, None)

    def __unicode__(self):
        return '%s - %s' %(self.user.username, self.name)

def _post_save_user(sender, **kwargs):
    if kwargs.get('created', None):
        user = kwargs.get('instance')
        for w in USER_WIDGETS:
            widget = USER_WIDGETS[w]
            app = App.objects.get(key_name=widget['app_id'])
            widget_obj = Widget(user=user, key_name=widget['id'], sort=widget['sort'], name=widget['name'], app=app)
            widget_obj.save()
        
post_save.connect(_post_save_user, sender=User)
