from django.conf import settings
from django.db import models
from yuntien.app.models.app import App
from yuntien.status.models.status import Status

class Like(models.Model):
    
    class Meta:
        app_label = 'status'
        ordering = ['-date_time']

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.ForeignKey(Status, related_name="%(app_label)s_%(class)s_set")
    app = models.ForeignKey(App, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
