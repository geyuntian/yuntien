from django.conf import settings
from django.db import models
from yuntien.authext.models.user import *

class RecordEntMixin(object):
    @classmethod
    def get_record_class(cls):
        return None
    
    def get_record_by_user(self, user):
        self.get_record_class().get_record(self, user)
        
    def add_record_by_user(self, user, operation):
        self.get_record_class().add_record(self, user, operation)

class RecordBase(models.Model):
    
    class Meta:
        abstract = True    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_set")
    operation = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_record(cls, obj, user):
        pass

    @classmethod
    def add_record(cls, obj, user, operation):
        pass
