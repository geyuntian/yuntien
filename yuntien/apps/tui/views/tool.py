from django.shortcuts import *
from django.template import RequestContext 
from django.utils.simplejson import *
from yuntien.apps.tui.context import PROCESSORS
from yuntien.apps.tui.settings import TEMPLATE_404, TEMPLATE_MESSAGE

def render(request, template, context={}):
    if isinstance(template, str) :
        rc = RequestContext(request, processors=PROCESSORS)
        return render_to_response(template, context, rc)
    else:
        return template(request, context)

def render_404(request, *args, **kwds):
    return render(request, TEMPLATE_404)

def render_message(request, message):
    context = { }
    context['message'] = message
    return render(request, TEMPLATE_MESSAGE, context)

def render_json(request, context):
    json = dumps(context)
    return HttpResponse(json, mimetype="application/json")
    