from django.shortcuts import *
from django.template import RequestContext 
from yuntien.apps.forum.context import PROCESSORS

def render(request, template, context={}):
    if isinstance(template, str) :
        rc = RequestContext(request, processors=PROCESSORS)
        return render_to_response(template, context, rc)
    else:
        return template(request, context)
