from django.conf.urls.defaults import *
from yuntien.community.main.views.tool import render
from yuntien.user.settings import USER_ID_REGEX, WIDGET_ID_REGEX

def r(template):
    def _r(request, context):
        return render(request, template, context)
    return _r

USER_ID = r'(?P<user>'+USER_ID_REGEX+r')'
FRIEND_ID = r'(?P<friend>'+USER_ID_REGEX+r')'
WIDGET = r'(?P<widget>'+WIDGET_ID_REGEX+r')'

USER_WIDGET_PREFIX = r'^'+USER_ID+r'/'+WIDGET

urlpatterns = patterns('yuntien.user.views',
    url(r'^'+USER_ID+r'$', 'statuses.user_timeline', {'render':r('user/statuses.html')}, name='user-display'),

    url(r'^'+USER_ID+r'/statuses$', 'statuses.user_timeline', {'render':r('user/statuses.html')}, name='user-statuses'),
    url(r'^'+USER_ID+r'/statuses/(?P<id>\d+)$', 'statuses.show', {'render':r('user/status.html')}, name='user-statuses-show'),
    url(r'^'+USER_ID+r'/statuses/post$', 'statuses.post', name='user-statuses-post'),

    url(r'^'+USER_ID+r'/friendships/create/'+FRIEND_ID+'$', 'friendships.create', name='friendships-create'),
    url(r'^'+USER_ID+r'/friendships/destroy/'+FRIEND_ID+'$', 'friendships.destroy', name='friendships-destroy'),
    
    url(USER_WIDGET_PREFIX+r'$', 'user.dispatch', {'render':r('user/dispatch.html')}, name='user-widget'),
    url(USER_WIDGET_PREFIX+r'/(?P<path>.+)$', 'user.dispatch', {'render':r('user/dispatch.html')}, name='user-dispatch'),
)
