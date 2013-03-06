from django import template
from django.template.defaultfilters import stringfilter
from yuntien.base.views.request import get_int_param

register = template.Library()

def _change_query_str(request, name, value):
    post = request.POST.copy()
    get = request.GET.copy()
    get.update(post)
    get[name] = str(value)
    query_str = get.urlencode() 
    return (request.path + '?' + query_str, query_str)

@register.filter
def previous_url(request):
    page = get_int_param(request, 'page', 1)
    url, qs = _change_query_str(request, 'page', page-1)    
    return url

@register.filter
def next_url(request):
    page = get_int_param(request, 'page', 1)
    url, qs = _change_query_str(request, 'page', page+1)    
    return url
