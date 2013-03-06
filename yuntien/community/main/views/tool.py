from django.shortcuts import *
from django.template import RequestContext 
from django.utils.simplejson import *
from yuntien.common.shortcuts import render_to_rich_response
from yuntien.community.main.context import PROCESSORS
from yuntien.community.main.settings import TEMPLATE_404, TEMPLATE_MESSAGE

def render(request, template, context={}, build_rc=None):
    if isinstance(template, str):
        if build_rc:
            rc = build_rc(request)
        else:
            rc = RequestContext(request, processors=PROCESSORS)
        return render_to_response(template, context, rc)
    else:
        return template(request, context)
    
def render_rich(request, template, context={}, build_rc=None):
    if build_rc:
        rc = build_rc(request)
    else:
        rc = RequestContext(request, processors=PROCESSORS)
    response = render_to_rich_response(template, context, rc)
    response.set_head(context.get('head', ''))
    response.set_title(context.get('title', ''))
    response.set_sidebar(context.get('sidebar', ''))
    return response

def render_404(request, *args, **kwds):
    return render(request, TEMPLATE_404)

def render_message(request, message):
    context = { }
    context['message'] = message
    return render(request, TEMPLATE_MESSAGE, context)

def render_json(request, context):
    json = dumps(context)
    return HttpResponse(json, mimetype="application/json")
    