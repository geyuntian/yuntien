from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls.defaults import *
from django.template import RequestContext 
from yuntien.apps.note.views.tool import render
from yuntien.apps.note.views.post import render_feed
from yuntien.community.main.urls import COMMUNITY, WIDGET
from yuntien.community.main.settings import COMMUNITY_PREFIX
from yuntien.community.main.views.tool import render_rich
from yuntien.user.settings import USER_PREFIX, USER_ID_REGEX
from yuntien.user.urls import USER_ID
from yuntien.app.settings import APP_API_STATUS_URL
from yuntien.apps.note.context import PROCESSORS

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

def r2(template):
    def _r(request, context):
        build_rc = lambda r: RequestContext(r, processors=PROCESSORS)
        response = render_rich(request, template, context, build_rc)
        return response
    return _r

def _status_url(request, status=None):
    if status.community:
        kwargs = {
            'community': status.community.key_name,
            'widget': status.community_widget.key_name,
            'id': status.object_id
            }
        return reverse('note-topic', urlconf='yuntien.apps.note.app', kwargs=kwargs, current_app='note')
    else:
        kwargs = {
            'user': status.user.username,
            'widget': status.user_widget.key_name,
            'id': status.object_id
            }
        return reverse('note-user-topic', urlconf='yuntien.apps.note.app', kwargs=kwargs, current_app='note')

PREFIX = r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'/'+WIDGET

USER_WIDGET_PREFIX = r'^'+USER_PREFIX+'/'+USER_ID+r'/'+WIDGET

urlpatterns = patterns('yuntien.apps.note.views',
    url(r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'$', 'post.list', {'render':r('note/app/widget.html'), 'num_per_page':3}, name='note-widget'),
    url(PREFIX+r'$', 'post.list', {'render':r('note/app/index.html')}, name='note-all'),
    url(PREFIX+r'/feed$', 'post.list', {'render':render_feed}, name='note-feed'),
    url(PREFIX+r'/(?P<id>\d+)$', 'post.display', {'render':r2('note/app/display.html')}, name='note-topic'),    
    url(PREFIX+r'/add$', 'post.add', {'render':r('note/app/add.html')}, name='note-add'),
    url(PREFIX+r'/edit/(?P<id>\d+)$', 'post.edit', {'render':r('note/app/edit.html')}, name='note-edit'),
    url(PREFIX+r'/delete/(?P<id>\d+)$', 'post.delete', name='note-delete'),

    url(r'^'+USER_PREFIX+'/'+USER_ID+'$', 'user.list_by_user_id', {'render':r('note/app/user_widget.html'), 'num_per_page':10}, name='note-user'),
    url(USER_WIDGET_PREFIX+'$', 'user.list_by_user_id', {'render':r('note/app/user_widget.html'), 'num_per_page':10}, name='note-user-widget'),
    url(USER_WIDGET_PREFIX+r'/(?P<id>\d+)$', 'post.display', {'render':r2('note/app/user_display.html')}, name='note-user-topic'),
    url(USER_WIDGET_PREFIX+r'/add$', 'user.add', {'render':r('note/app/user_add.html')}, name='note-user-add'),
    url(USER_WIDGET_PREFIX+r'/edit/(?P<id>\d+)$', 'user.edit', {'render':r('note/app/user_edit.html')}, name='note-user-edit'),
    url(USER_WIDGET_PREFIX+r'/delete/(?P<id>\d+)$', 'user.delete', name='note-user-delete'),
    
    url(r'^'+APP_API_STATUS_URL[1:]+r'$', _status_url),    
)
