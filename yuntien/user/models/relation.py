from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    
    class Meta:
        app_label = 'user'
        ordering = ['-date_time']
        unique_together = (("user1", "user2"),)

    user1 = models.ForeignKey(User, related_name="friend_set")
    user2 = models.ForeignKey(User, related_name="follower_set")
    type = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, user1, user2):
        f, created = cls.objects.get_or_create(user1=user1, user2=user2)
        return created
    
    @classmethod
    def destroy(cls, user1, user2):
        try:
            f = cls.objects.get(user1=user1, user2=user2)
            f.delete()
            return True
        except:
            return False
        
    @classmethod
    def exists(cls, user1, user2):
        try:
            cls.objects.get(user1=user1, user2=user2)
            return True
        except:
            return False

