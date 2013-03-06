# -*- coding:utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _
from django.utils import feedgenerator
from django.shortcuts import *
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from yuntien.common.markup import text_markup
from yuntien.base.views.request import check_request_method, get_int_param
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.status.models import Status
from yuntien.community.main.views.tool import render_404
from yuntien.status.views.util import get_status_url

class StatusForm(forms.Form):
    title = forms.CharField(required=True, max_length=140, widget=forms.Textarea)

def public_timeline(request, render, num_per_page=50):
    p = Paginator(Status.objects.all(), num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    statuses = page.object_list
    
    context = {
        'page_info': page,
        'statuses': statuses
    }
    return render(request, context)

def friends_timeline(request, render, num_per_page=50):
    if not request.user.is_authenticated():
        return render_404(request)
    
#    q = Status.objects.raw('SELECT * FROM status_status AS t1, user_relation AS t2 WHERE t1.user_id = t2.user2_id AND t2.user1_id = %s ORDER BY t1.date_time DESC LIMIT 50', [str(request.user.id)])
    q = Status.objects.raw('SELECT * FROM status_status AS t1, user_relation AS t2 WHERE t1.user_id = t2.user2_id AND t2.user1_id = %s ORDER BY t1.date_time DESC LIMIT '+str(num_per_page), [str(request.user.id)])
    context = {
        'page_info': None,
        'statuses': q
    }    
    return render(request, context)

@check_request_method(methods=('POST'))
@check_user()
def repost(request, id):    
    form = StatusForm(request.POST)    
    if form.is_valid():
        status = Status.objects.get(pk=id)
        status.repost(request.user, form.cleaned_data['title'])
        return HttpResponse('Done!')
    return HttpResponseNotFound()

def render_atom(request, context, title, descr):
    f = feedgenerator.Atom1Feed(
        title=title, 
        link=request.host_url, 
        description=descr,
        feed_url=request.build_absolute_uri(request.host_url))

    for status in context['statuses']:
        f.add_item(
            title=status.title, 
            link=request.host_url+get_status_url(status),
            description=status.title,
            author_name=status.user.username,
            author_link=request.host_url+reverse('user-display', kwargs={'user':status.user.username}),
            pubdate=status.date_time)
        
    return HttpResponse(f.writeString('UTF-8') , mimetype="application/atom+xml")
