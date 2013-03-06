from django.db import models
from django.utils import simplejson

class JSONMixin(models.Model):    

    class Meta:
        abstract = True
    
    json = models.TextField(blank=True)

    def get_json(self):
        return simplejson.loads(self.json)
    
    def set_json(self, json):
        self.json = simplejson.dumps(json)
        
class JSONBase(models.Model):

    class Meta:
        abstract = True
    
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    json = models.TextField(blank=True)
