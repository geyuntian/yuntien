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
    url(r'^login/$', 'accounts.login', name='accounts-login'),
    url(r'^register/$', 'accounts.register', {'render':r('user/register.html')}, name='accounts-register'),   
    url(r'^settings$', 'user.set_user_info', {'render':r('user/details.html')}, name='accounts-settings'),
    url(r'^settings/photo$', 'settings.set_photo', {'render':r('user/photo.html')}, name='accounts-settings-photo'),
)

urlpatterns += patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='accounts-logout'),   
)
