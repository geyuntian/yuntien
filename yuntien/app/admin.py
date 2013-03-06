from django.contrib import admin
from yuntien.app.models.app import App, Tag

class AppAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass
    
class TagAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

admin.site.register(App, AppAdmin)
admin.site.register(Tag, TagAdmin)
