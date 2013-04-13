from django.contrib import admin
from yuntien.apps.forum.models import Topic, Comment

class TopicAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
