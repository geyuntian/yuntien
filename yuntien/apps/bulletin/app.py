from django.conf.urls.defaults import *
from django.shortcuts import *
from yuntien.community.main.urls import COMMUNITY
from yuntien.community.main.settings import COMMUNITY_PREFIX

def r(template):
    def _r(request, context):
        return render_to_response(template, context)
    return _r

urlpatterns = patterns('yuntien.apps.bulletin.views',
    url(r'^'+COMMUNITY_PREFIX+'/'+COMMUNITY+r'$', 'board.show', {'render':r('bulletin/app/show.html')}, name='bulletin-widget'),
)
