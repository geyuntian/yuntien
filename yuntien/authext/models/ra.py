# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from yuntien.common.exceptions import YTError

class RAEntMixin(object):
    
    def get_role(self, user):
        pass

#Role assignment
class RABase(models.Model):
    
    class Meta:
        abstract = True
        ordering = ['-date_time']
        get_latest_by = "date_time"
            
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_set")
    date_time = models.DateTimeField(auto_now_add=True)
