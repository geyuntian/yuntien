import copy
from yuntien.authext.models.auth import AuthCheckParent
from yuntien.base.models.post import *
from yuntien.base.models.comment import *
from yuntien.base.models.category import *
from yuntien.community.main.models.community import Community, Widget
from yuntien.status.models import Status, SOURCE_TYPE_COMMUNITY

class Topic(PostBase):
    
    class Meta(PostBase.Meta):
        app_label = 'forum'
        
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    status = models.ForeignKey(Status, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    
    @classmethod
    def get_category_class(cls):
        return Category 
        
    @classmethod
    def get_comment_class(cls):
        return Comment
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.community  
      
    def delete(self):
        try:
            self.status.delete()
        except:
            pass
        super(Topic, self).delete()
            
    def save(self, *args, **kwargs):        
        add_status = not self.id
        super(Topic, self).save(*args, **kwargs) 
        if add_status:        
            s = Status()
            s.user = self.author
            s.app = self.community_widget.app
            s.source_type = SOURCE_TYPE_COMMUNITY
            s.source_id = self.community.id
            s.source_widget_id = self.community_widget.id
            
            s.object_id = self.id
            s.title = self.title
            s.save()
            self.status = s
            super(Topic, self).save(*args, **kwargs) 
    
class Category(CategoryBase):
    class Meta(CategoryBase.Meta):
        app_label = 'forum'

class Comment(CommentBase):

    class Meta(CommentBase.Meta):
        app_label = 'forum'
        
    topic = models.ForeignKey(Topic)
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)    
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.community
