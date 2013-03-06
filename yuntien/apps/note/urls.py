from django.conf.urls.defaults import *
from yuntien.apps.note.views.tool import render
from yuntien.apps.note.views.post import render_feed

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

urlpatterns = patterns('yuntien.apps.note.views',
    url(r'^$', 'post.list', {'render':r('note/index.html')}, name='note-list'),
    url(r'^feed$', 'post.list', {'render':render_feed}, name='note-feed'),

    url(r'^comment/(?P<id>\d+)$', 'comment.add', name='note-comment-add'),                    
    url(r'^comment/delete/(?P<id>\d+)$', 'comment.delete', name='note-comment-delete'),
)
