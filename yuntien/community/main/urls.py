from django.conf.urls import *
from yuntien.community.main.views.tool import render
from yuntien.community.main.settings import COMMUNITY_REGEX, WIDGET_ID_REGEX, AREA_ID_REGEX

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

COMMUNITY = r'(?P<community>'+COMMUNITY_REGEX+r')'
WIDGET = r'(?P<widget>'+WIDGET_ID_REGEX+r')'
AREA = r'(?P<area>'+AREA_ID_REGEX+r')'

urlpatterns = patterns('yuntien.community.main.views',
    url(r'^$', 'community.list_by_tags', {'render':r('main/list_by_tags.html')}, name='community-list'),
    url(r'^all$', 'community.all', {'render':r('main/all.html')}, name='community-all'),
    url(r'^add$', 'community.add', {'render':r('main/add.html')}, name='community-add'),

    url(r'^'+COMMUNITY+r'$', 'community.display', {'render':r('main/display.html')}, name='community-display'),
    
    url(r'^'+COMMUNITY+r'/admin/edit$', 'community.edit', {'render':r('main/edit.html')}, name='community-edit'),
    url(r'^'+COMMUNITY+r'/admin/settings/logo$', 'settings.set_logo', {'render':r('main/settings_logo.html')}, name='community-settings-logo'),
#    url(r'^'+COMMUNITY+r'/admin/delete$', 'community.delete', name='community-delete'),
    
    url(r'^'+COMMUNITY+r'/admin/area/all$', 'area.list', {'render':r('main/area/list.html')}, name='area-list'),
    url(r'^'+COMMUNITY+r'/admin/area/add$', 'area.add', {'render':r('main/area/add.html')}, name='area-add'),
    url(r'^'+COMMUNITY+r'/admin/area/edit/'+AREA+'$', 'area.edit', {'render':r('main/area/edit.html')}, name='area-edit'),
    
    url(r'^'+COMMUNITY+r'/admin/widget/all$', 'widget.list', {'render':r('main/widget/list.html')}, name='widget-list'),
    url(r'^'+COMMUNITY+r'/admin/widget/add$', 'widget.add', {'render':r('main/widget/add.html')}, name='widget-add'),
    url(r'^'+COMMUNITY+r'/admin/widget/edit/'+WIDGET+'$', 'widget.edit', {'render':r('main/widget/edit.html')}, name='widget-edit'),

    url(r'^'+COMMUNITY+r'/members/join$', 'community.join', name='community-join'),
    url(r'^'+COMMUNITY+r'/members/leave$', 'community.leave', name='community-leave'),
    
    url(r'^'+COMMUNITY+r'/area/'+AREA+'$', 'community.display', {'render':r('main/display.html')}, name='area-display'),
    
    url(r'^'+COMMUNITY+r'/'+WIDGET+r'$', 'community.dispatch', {'render':r('main/dispatch.html')}, name='community-widget'),
    url(r'^'+COMMUNITY+r'/'+WIDGET+r'/(?P<path>.+)$', 'community.dispatch', {'render':r('main/dispatch.html')}, name='community-dispatch'),
)
