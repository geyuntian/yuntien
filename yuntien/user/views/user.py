# -*- coding:utf-8 -*-
import copy
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from django.contrib.auth import get_user_model
from yuntien.common.markup import text_markup
from yuntien.common.exceptions import YTError
from yuntien.common.http import HttpResponseDirectOutput, HttpResponseRichOutput
from yuntien.authext.views.decorators import check_authorization, check_user, check_username
from yuntien.community.main.views.tool import render_404
from yuntien.user.settings import APPS, USER_ID_REGEX, RESERVED_USER_IDS, USER_WIDGETS

class UserForm(forms.Form):
    description = forms.CharField(required=False, widget=forms.Textarea)

@check_user()
def set_user_info(request, render):
    user_obj = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_obj.description = text_markup.render( form.cleaned_data['description'] )
            user_obj.raw_description = form.cleaned_data['description']
            user_obj.save()
            url = reverse('user-display', kwargs={'user':user_obj.username})
            return HttpResponseRedirect(url)
    else:
        form = UserForm(initial={'description':user_obj.raw_description}) # An unbound form

    context = {'form': form, 'user_obj':user_obj}
    return render(request, context)    

@check_username()
def display(request, render, user):
    user_obj = get_user_model().objects.get(username=user)
    widget = user_obj.user_widget_set.all()[0].key_name
    return dispatch(request, render, user, widget)

@check_username()
def dispatch(request, render, user, widget, path=''):
    user_obj = get_user_model().objects.get(username=user)
    user_obj.latest_communities = [ra.obj for ra in user_obj.main_ra_set.all()[:12]]
    
    if not widget in USER_WIDGETS:
        return render_404(request)

    w = copy.deepcopy(USER_WIDGETS[widget])
    app_config = APPS[w['app_id']]
    
    title = ''
    head = ''
    sidebar = ''
    
    view, args, kwargs = resolve(request.path, app_config['urls'])
    response = view(request, *args, **kwargs)
    if isinstance(response, HttpResponseRedirect):
        return response
    elif isinstance(response, HttpResponseDirectOutput):
        return response
    elif isinstance(response, HttpResponseRichOutput):
        w['content'] = response.content
        title = response.get_title()
        head = response.get_head()
        sidebar = response.get_sidebar()
    else:
        w['content'] = response.content
        
    context = {
        'title':title,
        'head':head,
        'sidebar':sidebar,
        'widget':w,
        'app':app_config,
        'user_obj':user_obj,
        'community_user': user_obj,
    }
    return render(request, context)
