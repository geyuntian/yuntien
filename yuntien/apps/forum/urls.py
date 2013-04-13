from django.conf.urls import *
from yuntien.apps.forum.views.tool import render

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

urlpatterns = patterns('yuntien.apps.forum.views',
    (r'^$', 'post.list', {'render':r('forum/all.html')}),
    (r'^delete/(?P<id>\d+)$', 'post.delete'),
#    (r'^stick/(?P<id>\d+)$', 'post.stick'),
#    (r'^unstick/(?P<id>\d+)$', 'post.unstick'),
    (r'^comment/(?P<id>\d+)$', 'comment.add'),                    
    (r'^comment/delete/(?P<id>\d+)$', 'comment.delete'),                    
)
