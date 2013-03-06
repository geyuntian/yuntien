import urllib
from django.shortcuts import *
from django.template import RequestContext 
from django.utils.simplejson import *
from django.core.urlresolvers import reverse
from django import forms
from yuntien.authext.views.decorators import check_authorization
from yuntien.authext.models.auth import OPERATION_ADD, OPERATION_DELETE
from yuntien.base.models.comment import *
from yuntien.base.views.decorators.db import *
from yuntien.apps.note.context import *
from yuntien.apps.note.settings import RECENT_COMMENT_NUM
from yuntien.apps.note.models import Topic, Comment
from yuntien.common.markup import text_markup

class CommentForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)

@check_authorization(Comment, OPERATION_ADD)
def add(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Topic.objects.get(pk=id)
            comment = Comment(topic=post, author=request.user)
            comment.content = text_markup.render( form.cleaned_data['content'] )
            comment.raw_content = form.cleaned_data['content']
            comment.community = post.community
            comment.community_widget = post.community_widget
            comment.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseNotFound()

@check_id(Comment)
@check_authorization(Comment, OPERATION_DELETE)
def delete(request, id):
    if request.method == 'POST':
        model = Comment.objects.get(pk=id)
        model.delete()
        return HttpResponse('Deleted!')
    return HttpResponseNotFound()
