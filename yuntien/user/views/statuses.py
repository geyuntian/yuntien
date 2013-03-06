# -*- coding:utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from django.http import HttpResponseNotFound 
from django.contrib.auth.models import User
from yuntien.common.markup import text_markup
from yuntien.status.models.status import Status
from yuntien.base.views.request import check_request_method, get_int_param
from yuntien.authext.views.decorators import check_authorization, check_user

class StatusForm(forms.Form):
    title = forms.CharField(required=True, max_length=140, widget=forms.Textarea)

def user_timeline(request, render, user, num_per_page=50):
    user_obj = User.objects.get(username=user)
    user_obj.latest_communities = [ra.obj for ra in user_obj.main_ra_set.all()[:12]]
    
    p = Paginator(user_obj.status_set.all(), num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    statuses = page.object_list
    
    context = {
        'user_obj':user_obj,
        'community_user': user_obj,
        'page_info': page,
        'statuses': statuses,
        'status_form': StatusForm()
    }
    return render(request, context)

def show(request, user, id, render):
    status = Status.objects.get(pk=id)
    context = {
        'user_obj':status.user,
        'community_user': status.user,
        'page_info': None,
        'status': status
    }
    return render(request, context)

def _get_user(request, *args, **kwds):
    u = request.user
    if u:
        return u.username == kwds.get('user', '')
    return False

@check_request_method(methods=('POST'))
@check_user(func=_get_user)
def post(request, user):    
    form = StatusForm(request.POST)    
    if form.is_valid():
        status = Status(user=request.user)
        status.title = form.cleaned_data['title']
        status.save()
        redirect = reverse('user-statuses', kwargs={'user':user})
        return HttpResponseRedirect(redirect)        
    return HttpResponseNotFound()
