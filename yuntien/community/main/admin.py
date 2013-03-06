from django.contrib import admin
from yuntien.community.main.models.community import Community, Tag, Area, Widget

class CommunityAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass
    
class TagAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

class AreaAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

class WidgetAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

admin.site.register(Community, CommunityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Widget, WidgetAdmin)
