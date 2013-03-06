import urllib2
from django.contrib.contenttypes.models import ContentType
from yuntien.authext.models.auth import AuthCheckParent
from yuntien.util import url
from yuntien.base.models.post import *
from yuntien.base.models.comment import *
from yuntien.base.models.vote import *
from yuntien.base.models.record import RecordBase
from yuntien.base.models.image import *
from yuntien.community.main.models.community import Community, Widget
from yuntien.status.models import Status, SOURCE_TYPE_COMMUNITY

class Domain(models.Model):
    
    class Meta:
        app_label = 'tui'
        
    domain_name = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    raw_description = models.TextField(blank=True)
    
    count = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_domain(cls, domain_name):
        try:
            return Domain.objects.get(domain_name=domain_name)
        except:
            d = Domain(domain_name=domain_name)
            d.save()
            return d
        
    def __unicode__(self):
        return self.domain_name

class Topic(VoteBase, ImageMixin, PostBase):
    
    class Meta(PostBase.Meta):
        app_label = 'tui'
        
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    status = models.ForeignKey(Status, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    
    comment_count = models.IntegerField(default=0)    
    domain = models.ForeignKey(Domain, blank=True, null=True)
    
    @property
    def thumbnail_name(self):
        return u'thumbnail/tui/%d.jpg' % self.id
    
    @property
    def thumbnail_url(self):
        return default_storage.url(self.thumbnail_name)
    
    @property
    def large_name(self):
        return u'large/tui/%d.jpg' % self.id

    @property
    def large_url(self):
        return default_storage.url(self.large_name)

    @property
    def medium_name(self):
        return u'medium/tui/%d.jpg' % self.id        
    
    @property
    def medium_url(self):
        return default_storage.url(self.medium_name)        
    
    @classmethod
    def get_record_class(cls):
        return Record
    
    @classmethod
    def get_comment_class(cls):
        return Comment
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.community 
    
    def is_valid(self):
        if self.type == TYPE_INVALID:
            return False
        return True
    
    def delete(self, check_children=False):
#        if self.type != TYPE_INVALID:
#            self.get_tag_class().remove_tags(self.tags)
#            if self.category:
#                category = self.get_category_class().get_by_key_name(self.category)
#                if category:
#                    category.count -= 1
#                    category.put()

        try:
            self.status.delete()
        except:
            pass
        
        if self.has_image:
            default_storage.delete(self.thumbnail_name)
            default_storage.delete(self.large_name)
            default_storage.delete(self.medium_name)            
        
        #to avoid dead children comments
        if check_children and self.comment_count > 0:
            self.type = TYPE_INVALID
            super(Topic, self).save()
        else:
            super(Topic, self).delete()
            
    def save(self, *args, **kwargs):     
        add_status = not self.id   
        if self.link and not self.domain:
            self.domain = Domain.get_domain(get_domain(self.link))
            self.domain.count += 1
            self.domain.save()
        self.handle_link()
        super(Topic, self).save(*args, **kwargs)
        #also called in update? sometimes necessary.
        self.download_image()
        
        if add_status:        
            s = Status()
            s.user = self.author
            s.app = self.community_widget.app
            s.source_type = SOURCE_TYPE_COMMUNITY
            s.source_id = self.community.id
            s.source_widget_id = self.community_widget.id

            s.content_type = ContentType.objects.get_for_model(Topic)
            s.object_id = self.id
            s.title = self.title
            s.save()
            self.status = s
            super(Topic, self).save(*args, **kwargs)    
            
    def handle_link(self):
        headers = {}
        try:
            headers = urllib2.urlopen(url.HeadRequest(self.link)).headers.dict
        except:
            pass
        
        if 'content-type' in headers and 'image/' in headers['content-type']:
            
            try:
                size = int(headers['content-length'])
                #large image
                if size > 1024*1024*2:
                    return
            except:
                return
            
            self.type = TYPE_HAS_IMAGE

    def download_image(self):
        if self.type == TYPE_HAS_IMAGE:           
            try:
                file = urllib2.urlopen(self.link)
                content_file = ContentFile(file.fp.read())
                handler1 = SquareImageHandler(self.thumbnail_name, 180) 
                handler2 = FixedWidthImageHandler(self.large_name, 800, 10000) 
                handler3 = FixedWidthImageHandler(self.medium_name, 180, 600)
                self.save_image(content_file, (handler1, handler2, handler3))                
            except:
                self.type = TYPE_NORMAL
                super(Topic, self).save(*args, **kwargs)

class Record(RecordBase):
    obj = models.ForeignKey(Topic)
    
    @classmethod
    def get_record(cls, obj, user):
        try:
            return cls.objects.filter(obj=obj).filter(user=user).get()
        except:
            return None            

    @classmethod
    def add_record(cls, obj, user, operation):
        r = cls(obj=obj, user=user, operation=operation)
        r.save()

class Comment(VoteBase, CommentBase):

    class Meta(PostBase.Meta):
        app_label = 'tui'
        
    topic = models.ForeignKey(Topic)
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    comment_count = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    
    @classmethod
    def get_record_class(cls):
        return CommentRecord
    
    @classmethod
    def get_comment_class(cls):
        return Comment
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.community  
    
    def is_valid(self):
        if self.type == TYPE_INVALID:
            return False
        return True
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.topic.comment_count += 1
            self.topic.save()
            
            if self.parent:
                self.parent.comment_count += 1
                self.parent.save()
           
        super(Comment, self).save(*args, **kwargs)
        
    def delete(self, check_children=False):
        self.topic.comment_count -= 1
        self.topic.save()
        
        if self.parent:
            self.parent.comment_count -= 1
            self.parent.save()      
        
        #to avoid dead children comments
        if check_children and self.comment_count > 0:
            self.type = TYPE_INVALID
            super(Comment, self).save()
        else:
            super(Comment, self).delete()        
   
class CommentRecord(RecordBase):
    obj = models.ForeignKey(Comment)
    
    @classmethod
    def get_record(cls, obj, user):
        try:
            return cls.objects.filter(obj=obj).filter(user=user).get()
        except:
            return None            

    @classmethod
    def add_record(cls, obj, user, operation):
        r = cls(obj=obj, user=user, operation=operation)
        r.save()
