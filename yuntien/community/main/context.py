from yuntien.base.views.plugin import plugin as _plugin
from yuntien.base.views.plugin import *
#from yuntien.community.main.settings import USER_WIDGETS
from yuntien.community.main.settings import *
from yuntien.community.common.settings import APPS, RESOURCE_URL

def get(request):
    context = {}
    page = request.GET.get('page', '1')
    context['page'] = int(page)
    context['tag'] = request.GET.get('tag', '')
    return context

def config(request):
    context = {}
    context['config'] = CONFIG
    context['resource_url'] = RESOURCE_URL
    return context

def apps(request):
    context = {}
    context['apps'] = APPS
    context['apps_sorted'] = [APPS[app] for app in sorted(APPS, key=lambda app: APPS[app]['sort'])]    
#    context['user_widgets'] = USER_WIDGETS
#    context['user_widgets'] = [USER_WIDGETS[w] for w in sorted(USER_WIDGETS, key=lambda w: USER_WIDGETS[w]['sort'])]    
    return context

def auth(request):
    context = {}
    return context

def plugin(request):
    return _plugin(request, PLUGINS, [TYPE_SIDE, TYPE_TOP, TYPE_BOTTOM])

PROCESSORS = [get, config, auth, plugin]
