from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls import *
from django.template import RequestContext
from yuntien.apps.forum.views.tool import render
from yuntien.community.main.urls import COMMUNITY, WIDGET
#from yuntien.community.main.user import USER_ID
from yuntien.community.main.settings import COMMUNITY_PREFIX#, USER_PREFIX
from yuntien.community.main.views.tool import render_rich
from yuntien.app.settings import APP_API_STATUS_URL
from yuntien.apps.forum.context import PROCESSORS

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
    kwargs = {
        'community': status.community.key_name,
        'widget': status.community_widget.key_name,
        'id': status.object_id
        }
    return reverse('forum-topic', urlconf='yuntien.apps.forum.app', kwargs=kwargs, current_app='forum')

PREFIX = r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'/'+WIDGET

urlpatterns = patterns('yuntien.apps.forum.views',
    url(r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'$', 'post.list', {'render':r('forum/app/widget.html'), 'num_per_page':10}, name='forum-widget'),
    url(PREFIX+r'$', 'post.list', {'render':r('forum/app/index.html')}, name='forum-all'),

    url(PREFIX+r'/(?P<id>\d+)$', 'post.display', {'render':r2('forum/app/display.html')}, name='forum-topic'),
    url(PREFIX+r'/add$', 'post.add', {'render':r('forum/app/add.html')}, name='forum-add'),
    url(PREFIX+r'/edit/(?P<id>\d+)$', 'post.edit', {'render':r('forum/app/edit.html')}, name='forum-edit'),

#    url(r'^'+USER_PREFIX+'/'+USER_ID+r'$', 'post.list_by_user_id', {'render':r('forum/app/widget.html'), 'num_per_page':10}, name='forum-user'),

    url(r'^'+APP_API_STATUS_URL[1:]+r'$', _status_url),
)
