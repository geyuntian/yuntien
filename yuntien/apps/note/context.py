#from yuntien.base.models.auth import *
from yuntien.base.models.post import *
from yuntien.base.models.comment import *
from yuntien.base.views.plugin import plugin as _plugin
from yuntien.apps.note.settings import *
from yuntien.apps.note.models import Topic, Comment

def get(request):
    context = {}
    page = request.GET.get('page', '1')
    context['page'] = int(page)
    context['comment_num_per_page'] = 10
    context['tag'] = request.GET.get('tag', '')
    return context

def config(request):
    context = {}
    context['config'] = CONFIG
    context['app_id'] = APP_ID
    return context

def auth(request):
    context = {}
    context['auth'] = Topic.get_auth_class().get_auth()
    context['auth_comment'] = Comment.get_auth_class().get_auth()
    return context

def plugin(request):
    return _plugin(request, PLUGINS, [TYPE_SIDE, TYPE_TOP, TYPE_BOTTOM, TYPE_POST_BOTTOM])

PROCESSORS = [get, config, auth, plugin]
