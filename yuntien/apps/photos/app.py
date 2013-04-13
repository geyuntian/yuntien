from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls import *
from django.template import RequestContext
from yuntien.apps.photos.views.tool import render
from yuntien.community.main.urls import COMMUNITY, WIDGET
#from yuntien.community.main.user import USER_ID
from yuntien.community.main.settings import COMMUNITY_PREFIX#, USER_PREFIX
from yuntien.app.settings import APP_API_STATUS_URL, APP_API_STATUS_RENDER
from yuntien.apps.photos.models.photo import Photo

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

def _status_url(request, status=None):
    kwargs = {
        'community': status.source.key_name,
        'widget': status.source_widget.key_name,
        'id': status.object_id
        }
    return reverse('photos-photo', urlconf='yuntien.apps.photos.app', kwargs=kwargs, current_app='photos')

def _render_status(request, status=None):
    kwargs = {
        'status': status,
        }
    return render(request, 'photos/app/status.html', kwargs)

PREFIX = r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'/'+WIDGET

urlpatterns = patterns('yuntien.apps.photos.views',
    url(r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'$', 'photos.list', {'render':r('photos/app/widget.html'), 'num_per_page':10}, name='photos-widget'),
    url(PREFIX+r'$', 'photos.list', {'render':r('photos/app/widget.html')}, name='photos-all'),

    url(PREFIX+r'/(?P<id>\d+)$', 'photos.show', {'render':r('photos/app/show.html')}, name='photos-photo'),
    url(PREFIX+r'/add$', 'photos.add', {'render':r('photos/app/add.html')}, name='photos-add'),
    url(PREFIX+r'/(?P<id>\d+)/delete$', 'photos.delete', name='photos-delete'),

    url(r'^'+APP_API_STATUS_URL[1:]+r'$', _status_url),
    url(r'^'+APP_API_STATUS_RENDER[1:]+r'$', _render_status),
)
