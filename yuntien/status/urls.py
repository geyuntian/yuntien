from django.conf.urls import *
from yuntien.community.main.views.tool import render
from yuntien.community.main.settings import CONFIG
from yuntien.status.views.statuses import render_atom

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

def r2():
    def _r(request, context):
        return render_atom(request, context, CONFIG['site_title'], CONFIG['site_description'])
    return _r

urlpatterns = patterns('yuntien.status.views',
    url(r'^public_timeline$', 'statuses.public_timeline', {'render':r('status/statuses.html')}, name='statuses-public-timeline'),
    url(r'^public_timeline.atom$', 'statuses.public_timeline', {'render':r2()}),
    
    url(r'^friends_timeline$', 'statuses.friends_timeline', {'render':r('status/statuses.html')}, name='statuses-friends-timeline'),
    
    url(r'^repost/(?P<id>\d+)$', 'statuses.repost', name='statuses-repost'),       
)
