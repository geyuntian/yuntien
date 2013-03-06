from django.db import models

class CategoryBase(models.Model):
    
    class Meta:
        abstract = True
        ordering = ['-sort'] 
    
    key_name = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    count = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
