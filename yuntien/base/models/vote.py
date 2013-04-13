import datetime
from django.conf import settings
from django.db import models

class VoteBase(models.Model):
    
    class Meta:
        abstract = True
    
    vote_points = models.IntegerField(default=0)
    vote_quality = models.FloatField(default=0.0) 
    up_count = models.IntegerField(default=0)
    up_time = models.DateTimeField(blank=True, null=True)
    down_count = models.IntegerField(default=0)
    down_time = models.DateTimeField(blank=True, null=True)
    up_down_count = models.IntegerField(default=0)
    up_down_ratio = models.FloatField(default=99999999.0)
    
    def vote_up(self, user):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return
        
        r = self.get_record_class().get_record(self, user)
        if r:
            return
        
        self.up_count += 1
        self.up_time = datetime.datetime.now()
        self.up_down_count += 1
        self.up_down_ratio = self._calc_up_down_ratio()
        self.vote_points += 1
        self.vote_quality = self._calc_quality()
        self.save()

        self.get_record_class().add_record(self, user, 1)
            
    def vote_down(self, user):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return
        
        r = self.get_record_class().get_record(self, user)
        if r:
            return
        
        self.down_count += 1
        self.down_time = datetime.datetime.now()
        self.up_down_count += 1
        self.up_down_ratio = self._calc_up_down_ratio()
        self.vote_quality = self._calc_quality()
        self.vote_points -= 1
        self.save()
        
        self.get_record_class().add_record(self, user, 2)
        
    def _calc_up_down_ratio(self):
        if self.up_count == 0 or self.down_count == 0:
            return 99999999.0
        
        if self.up_count >= self.down_count:
            return self.up_count*1.0/self.down_count
        else:
            return self.down_count*1.0/self.up_count
        
    def _calc_quality(self):
        up = self.up_count
        if up == 0:
            up = 1
            
        down = self.down_count
        if down == 0:
            down = 1
            
        return up*1.0/down
