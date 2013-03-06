from django.db import models

DEFAULT = 0
MANAGED = 1

PUBLIC = 0
MEMBER_ONLY = 1
OWNER_ONLY = 2

class WidgetBase(models.Model):
    
    class Meta:
        abstract = True

    type = models.IntegerField(default=DEFAULT)
    privacy_type = models.IntegerField(default=MEMBER_ONLY)
