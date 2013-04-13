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
from yuntien.user.models import User

register = Library()

class HotNode(Node):
    def __init__(self, num, asvar):
        self.num = num
        self.asvar = asvar

    def render(self, context):
        try:
            num = int(self.num)
        except:
            num = Variable(self.num).resolve(context)

        objects = User.objects.all().order_by('-statuses_count')[:num]
        users = [obj for obj in objects if obj.statuses_count > 0]

        if self.asvar:
            context[self.asvar] = users
            return ''
        else:
            return users

def hot(parser, token):
    """
    {% hot_users num as var %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    num = bits[1]
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    return HotNode(num, asvar)

hot = register.tag('hot_users', hot)
