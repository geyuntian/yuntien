from django.contrib import admin
from yuntien.user.models.user import Widget

class WidgetAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

admin.site.register(Widget, WidgetAdmin)
