from django.db import models

class Text(models.Model):
    
    class Meta:
        app_label = 'common'
    
    text = models.TextField(blank=True)
    raw_text = models.TextField(blank=True)

class DescriptionBase(models.Model):
    
    class Meta:
        abstract = True

    text = models.ForeignKey(Text, blank=True, null=True)
