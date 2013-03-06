from django import template
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from yuntien.base.models.comment import *
from yuntien.apps.tui.views.comment import CommentForm

register = template.Library()

@register.filter
def render_comments(comment, template):
    c = {'comment':comment, 'form':CommentForm({})}
    c.update(csrf(comment.request))
    return render_to_string(template, c)
