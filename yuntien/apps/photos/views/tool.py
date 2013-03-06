from django.shortcuts import *
from django.template import RequestContext 
from yuntien.authext.models.auth import *
from yuntien.base.views.plugin import plugin as _plugin
from yuntien.apps.photos.settings import *
from yuntien.apps.photos.models import Photo

def config(request):
    context = {}
    context['app_id'] = APP_ID
    return context

def auth(request):
    context = {}
    context['auth'] = Photo.get_auth_class().get_auth()
    return context

PROCESSORS = [config, auth]

def render(request, template, context={}):
    if isinstance(template, str) :
        rc = RequestContext(request, processors=PROCESSORS)
        return render_to_response(template, context, rc)
    else:
        return template(request, context)
