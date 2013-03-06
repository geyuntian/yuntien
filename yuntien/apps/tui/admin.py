from django.contrib import admin
from yuntien.apps.tui.models import Topic, Comment

class TopicAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('title',)
    pass
    
#class TagAdmin(admin.ModelAdmin):
##    list_display = ('name',)
#    search_fields = ('name',)
#    pass
#
#class CategoryAdmin(admin.ModelAdmin):
##    list_display = ('name',)
#    search_fields = ('name',)
#    pass

class CommentAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#    search_fields = ('name',)
    pass

admin.site.register(Topic, TopicAdmin)
#admin.site.register(Tag, TagAdmin)
#admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
