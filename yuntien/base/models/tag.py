from django.db import models
from yuntien.base.settings import *

class TagEntMixin(object):
    @classmethod
    def get_tag_class(cls):
        return None
    
    @classmethod
    def get_tag_splitter(cls):
        return ' '
    
    def add_tags(self, tag_str):
        self._tag_str = tag_str

    def add_tags_to_db(self):
        if not hasattr(self, '_tag_str'):
            return
  
        if self._tag_str == self.get_tag_str():
            return
      
        #tag max number should be less than 10, for better performance
        tags = self._tag_str.split(self.get_tag_splitter())[0:MAX_TAG_NUM]
        #remove invalid tag
        tags = [tag for tag in tags if tag != '']
        current_tags = [tag.name for tag in self.tags.all()]
        #to add
        tags_new = [tag for tag in tags if tag not in current_tags]
        #to delete
        tags_old = [tag for tag in current_tags if tag not in tags]
        
        self.get_tag_class().add_tags(tags_new)
        self.get_tag_class().remove_tags(tags_old)
        
        self.tags = self.get_tag_class().objects.filter(name__in=tags)
    
    def get_tag_str(self):
        current_tags = [tag.name for tag in self.tags.all()]
        return self.get_tag_splitter().join(current_tags[0:MAX_TAG_NUM])
    
class TagBase(models.Model):

    class Meta:
        abstract = True
        ordering = ['-sort']
          
    name = models.CharField(max_length=30, primary_key=True)
    count = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

    @classmethod
    def add_tags(cls, tags):
        tag_infos = []
        try:
            for tag in tags:
                tag_info, created = cls.objects.get_or_create(name=tag)
                tag_info.count = tag_info.count + 1
                tag_info.save()
                tag_infos.append(tag_info)
        except:
            pass
        return tag_infos

    @classmethod
    def remove_tags(cls, tags):
        tag_infos = []
        try:
            for tag in tags:
                tag_info, created = cls.objects.get_or_create(name=tag)
                if tag_info and tag_info.count > 0: 
                    tag_info.count = tag_info.count - 1
                    tag_info.save()
                tag_infos.append(tag_info)
        except:
            pass
        return tag_infos
