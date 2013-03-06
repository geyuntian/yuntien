import sys
import re
from itertools import groupby, cycle as itertools_cycle

from django.template import Node, NodeList, Template, Context, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template import get_library, Library, InvalidTemplateLibrary
from django.template.smartif import IfParser, Literal
from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from yuntien.status.views.util import get_status_url, render_status

register = Library()
# Regex for token keyword arguments
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

class URLNode(Node):
    def __init__(self, status, asvar):
        self.status = status
        self.asvar = asvar

    def render(self, context):
        status = Variable(self.status).resolve(context)
        url = get_status_url(status)

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def url(parser, token):
    """
    {% status_url status %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    status = bits[1]
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    return URLNode(status, asvar)
url = register.tag('status_url', url)

render_status = register.simple_tag(render_status, takes_context=True)
