from django.conf.urls.defaults import *
from yuntien.apps.tui.views.tui import render_tui, render_feed
from yuntien.apps.tui.views.tool import render

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

urlpatterns = patterns('yuntien.apps.tui.views',
    url(r'^$', 'tui.list', {'render':r('tui/index.html')}, name='tui-all'),
#    url(r'^t/(?P<category>.+)$', 'tui.list_by_category', {'render':r('tui/index.html')}, name='tui-category'),
    url(r'^domain/(?P<domain>.+)$', 'tui.list_by_domain', {'render':r('tui/index.html')}, name='tui-domain'),
    url(r'^user/(?P<user>.+)$', 'tui.list_by_user_id', {'render':r('tui/index.html')}, name='tui-user'),
    url(r'^add$', 'tui.add', {'render':r('tui/add.html')}, name='tui-add'),
    url(r'^(?P<id>\d+)$', 'tui.display', {'render':r('tui/display.html')}, name='tui-topic'),
    (r'^delete/(?P<id>\d+)$', 'tui.delete'),
    (r'^up/(?P<id>\d+)$', 'tui.up'),
    (r'^down/(?P<id>\d+)$', 'tui.down'),
    (r'^comment/(?P<id>\d+)$', 'comment.add'),                    
    (r'^comment/(?P<id>\d+)/(?P<parent>\d+)$', 'comment.add'),                
    (r'^comment/display/(?P<id>\d+)$', 'tui.display_comment', {'render':r('tui/comment.html')}),
    (r'^comment/edit/(?P<id>\d+)$', 'comment.edit'),
    (r'^comment/delete/(?P<id>\d+)$', 'comment.delete'),
    (r'^comment/up/(?P<id>\d+)$', 'comment.up'),
    (r'^comment/down/(?P<id>\d+)$', 'comment.down'),
    url(r'^comment/latest', 'tui.list_latest_comments', {'render':r('tui/comment_list.html')}, name='tui-comment-latest'),

    url(r'^api/all$', 'tui.list', {'render':render_tui}, name='tui-api-all'),
#    url(r'^api/t/(?P<category>.+)$', 'tui.list_by_category', {'render':render_tui}, name='tui-api-category'),
    url(r'^api/domain/(?P<domain>.+)$', 'tui.list_by_domain', {'render':render_tui}, name='tui-api-domain'),
    url(r'^api/user/(?P<user>.+)$', 'tui.list_by_user_id', {'render':render_tui}, name='tui-api-user'),

    url(r'^feed/all$', 'tui.list', {'render':render_feed}, name='tui-feed-all'),
#    url(r'^feed/t/(?P<category>.+)$', 'tui.list_by_category', {'render':render_feed}, name='tui-feed-category'),
    url(r'^feed/domain/(?P<domain>.+)$', 'tui.list_by_domain', {'render':render_feed}, name='tui-feed-domain'),
    url(r'^feed/user/(?P<user>.+)$', 'tui.list_by_user_id', {'render':render_feed}, name='tui-feed-user'),
)
