from django.db import models
from django.contrib.contenttypes.models import ContentType
from yuntien.framework import settings

class SourceMixin(models.Model):
    
    class Meta:
        abstract = True

    source_type = models.IntegerField(default=settings.SOURCE_TYPE_DEFAULT)
    source_id = models.IntegerField(blank=True, null=True)
    source_widget_id = models.IntegerField(blank=True, null=True)
    
    @property
    def source(self):
        s = settings.SOURCE.get(self.source_type)['source']
        content_type = ContentType.objects.get_by_natural_key(s['app_label'], s['model'])
        source = content_type.model_class().objects.get(pk=self.source_id)
        return source
    
    @property
    def source_widget(self):
        s = settings.SOURCE.get(self.source_type).get('source_widget', None)
        if s:
            content_type = ContentType.objects.get_by_natural_key(s['app_label'], s['model'])
            source = content_type.model_class().objects.get(pk=self.source_widget_id)
            return source
