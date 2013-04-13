import copy
from django.conf import settings
from yuntien.authext.models.auth import AuthCheckParent
from yuntien.base.models.post import *
from yuntien.base.models.comment import *
from yuntien.base.models.category import CategoryBase
from yuntien.base.models.tag import TagBase
from yuntien.community.main.models.community import Community, Widget
from yuntien.user.models.widget import Widget as UserWidget
from yuntien.status.models import Status, SOURCE_TYPE_USER, SOURCE_TYPE_COMMUNITY

class Tag(TagBase):
    
    class Meta(TagBase.Meta):
        app_label = 'note'

class Topic(PostBase):
    
    class Meta(PostBase.Meta):
        app_label = 'note'
        
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_user_%(class)s_set", blank=True, null=True) 
    user_widget = models.ForeignKey(UserWidget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    status = models.ForeignKey(Status, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)
    
    @classmethod
    def get_tag_class(cls):
        return Tag
    
    @classmethod
    def get_category_class(cls):
        return Category 
        
#    @classmethod
#    def get_comment_class(cls):
#        return YTNoteComment
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent
    
    def get_auth_parent(self):
        return self.community

    def save(self, *args, **kwargs):
        add_status = not self.id
        super(Topic, self).save(*args, **kwargs)
        self.add_tags_to_db()
        
        if add_status:        
            s = Status()
            s.user = self.author
            if self.user_widget:
                s.app = self.user_widget.app
                s.source_type = SOURCE_TYPE_USER
                s.source_id = self.author.id
                s.source_widget_id = self.user_widget.id
            else:
                s.app = self.community_widget.app
                s.source_type = SOURCE_TYPE_COMMUNITY
                s.source_id = self.community.id
                s.source_widget_id = self.community_widget.id
                
            s.object_id = self.id
            s.title = self.title
            s.save()
            self.status = s     
        
        super(Topic, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        Tag.remove_tags([tag.name for tag in self.tags.all()])
        try:
            self.status.delete()
        except:
            pass       
        super(Topic, self).delete(*args, **kwargs)
    
class Category(CategoryBase):
    
    class Meta(CategoryBase.Meta):
        app_label = 'note'    

class Comment(CommentBase):
    
    class Meta(CommentBase.Meta):
        app_label = 'note'
        
    topic = models.ForeignKey(Topic)
    community = models.ForeignKey(Community, related_name="%(app_label)s_%(class)s_set", blank=True, null=True) 
    community_widget = models.ForeignKey(Widget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_user_%(class)s_set", blank=True, null=True) 
    user_widget = models.ForeignKey(UserWidget, related_name="%(app_label)s_%(class)s_set", blank=True, null=True)
    
    @classmethod
    def get_auth_class(cls):
        return AuthCheckParent

    def get_auth_parent(self):
        return self.community
