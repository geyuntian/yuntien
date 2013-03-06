import urllib
from django.shortcuts import *
from django.template import RequestContext 
from django.utils.simplejson import *
from django.core.urlresolvers import reverse
from django import forms
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.base.models.comment import *
from yuntien.base.views.decorators.db import *
from yuntien.authext.models.auth import *
from yuntien.apps.tui.settings import RECENT_COMMENT_NUM
from yuntien.apps.tui.context import *
from yuntien.apps.tui.models import *
from yuntien.common.markup import text_markup
from django.utils.html import strip_tags
from tool import *

class CommentForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)
    
@check_authorization(Comment, OPERATION_ADD)
def add(request, id, parent=''):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Topic.objects.get(id=id)
            p = post
            comment = Comment(topic=post)
            comment.community = post.community
            comment.community_widget = post.community_widget
            comment.author = request.user
            comment.content = text_markup.render( strip_tags(form.cleaned_data['content']) )
            comment.raw_content = form.cleaned_data['content']
            
            if parent:
                c = Comment.objects.get(id=parent)
                if c:
                    comment.parent = c
                    comment.level = c.level + 1
            
            comment.save()
#            deferred.defer(_calc_total_points, comment.key().id())
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseNotFound()

@check_id(Comment)
@check_authorization(Comment, OPERATION_EDIT)
def edit(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(id=id)
            comment.content = text_markup.render( strip_tags(form.cleaned_data['content']) )
            comment.raw_content = form.cleaned_data['content']
#            comment.save(add_version=True)
            comment.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseNotFound()

@check_id(Comment)
@check_authorization(Comment, OPERATION_DELETE)
def delete(request, id):
    if request.method == 'POST':
        tui = Comment.objects.get(id=id)
        tui.delete(check_children=True)
        return HttpResponse('Done!')
    return render_404()

@check_id(Comment)
@check_user()
def up(request, id):
    if request.method == 'POST':
        tui = Comment.objects.get(id=id)
        tui.vote_up(request.user)
#        deferred.defer(_calc_total_points, tui.key().id())
        return HttpResponse('Done!')
    return render_404()

@check_id(Comment)
@check_user()
def down(request, id):
    if request.method == 'POST':
        tui = Comment.objects.get(id=id)
        tui.vote_down(request.user)
#        deferred.defer(_calc_total_points, tui.key().id())
        return HttpResponse('Done!')
    return render_404()

def _calc_total_points(id):
    c = Comment.objects.get(id=id)
    c.calc_total_points()
