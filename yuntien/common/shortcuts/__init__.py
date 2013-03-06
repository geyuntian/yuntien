from django.template import loader
from yuntien.common.http import HttpResponseRichOutput

def render_to_rich_response(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    return HttpResponseRichOutput(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)
