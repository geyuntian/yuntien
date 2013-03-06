from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls.defaults import *
from yuntien.apps.tui.views.tui import render_tui, render_feed
from yuntien.apps.tui.views.tool import render
from yuntien.community.main.urls import COMMUNITY, WIDGET
from yuntien.user.urls import USER_ID
from yuntien.user.settings import USER_PREFIX
from yuntien.community.main.settings import COMMUNITY_PREFIX
from yuntien.app.settings import APP_API_STATUS_URL, APP_API_STATUS_RENDER

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

def _status_url(request, status=None):
    kwargs = {
        'id': status.object_id
        }
    return reverse('tui-topic', kwargs=kwargs, current_app='tui')

def _render_status(request, status=None):
    kwargs = {
        'status': status,
        }
    return render(request, 'tui/app/status.html', kwargs)

PREFIX = r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'/'+WIDGET

urlpatterns = patterns('yuntien.apps.tui.views',
#    url(r'^'+COMMUNITY_PREFIX+'/$', 'tui.list', {'render':r('tui/app/widget.html'), 'num_per_page':10}, name='tui-summary'),

    url(r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'$', 'tui.list', {'render':r('tui/app/widget.html'), 'home':True}, name='tui-widget'),
    url(PREFIX+r'$', 'tui.list', {'render':r('tui/app/index.html')}, name='tui-all'),
    url(PREFIX+r'/add$', 'tui.add_in_widget', {'render':r('tui/app/add.html')}, name='tui-add'),
    
    url(r'^'+APP_API_STATUS_URL[1:]+r'$', _status_url),
    url(r'^'+APP_API_STATUS_RENDER[1:]+r'$', _render_status),
)
