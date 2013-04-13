from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from yuntien.user.models.user import User
from yuntien.user.models.widget import Widget

class WidgetAdmin(admin.ModelAdmin):
#    list_display = ('name',)
    search_fields = ('name',)
    pass

admin.site.register(Widget, WidgetAdmin)
admin.site.register(User, UserAdmin)
