# -*- coding:utf-8 -*-
import copy
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from yuntien.common.markup import text_markup
from yuntien.authext.views.decorators import check_authorization
from yuntien.authext.models.auth import OPERATION_EDIT
from yuntien.base.views.decorators.db import check_name
from yuntien.community.main.models.community import Community, Area
from yuntien.community.common.settings import AREA_ID_REGEX

def _find_community(cls, request, *args, **kwds):
    if kwds.has_key('community'):
        return Community.objects.get(key_name=kwds['community'])
          
@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def add(request, community, render):
    c = Community.objects.get(key_name=community)
    
    def _validate_area_id(value):
        if value:
            try:
                c.area_set.get(key_name=value)
                raise ValidationError(_(u'%s is already used.') % value)
            except Area.DoesNotExist:
                pass
    
    class AreaForm(forms.Form):
        area_id = forms.RegexField(regex='^'+AREA_ID_REGEX+'$', required=True, validators=[_validate_area_id])
        name = forms.CharField(required=True, max_length=10)
        description = forms.CharField(required=False, widget=forms.Textarea)
        sort = forms.IntegerField(required=True, initial=0)
    
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            area = Area(key_name=form.cleaned_data['area_id'], name=form.cleaned_data['name'])
            area.description = text_markup.render( form.cleaned_data['description'] )
            area.raw_description = form.cleaned_data['description']
            area.sort = form.cleaned_data['sort']
            area.community = c
            area.save()
            
            url = reverse('community-display', kwargs={'community':community})
            return HttpResponseRedirect(url)
    else:
        form = AreaForm() # An unbound form

    context = {'form': form, 'community_obj':c}
    return render(request, context)

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def edit(request, community, area, render):
    c = Community.objects.get(key_name=community)
    a = c.area_set.get(key_name=area)
    
    class AreaForm(forms.Form):
        name = forms.CharField(required=True, max_length=10)
        description = forms.CharField(required=False, widget=forms.Textarea)
        sort = forms.IntegerField(required=True, initial=0)

    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            a.name = form.cleaned_data['name']
            a.description = text_markup.render( form.cleaned_data['description'] )
            a.raw_description = form.cleaned_data['description']
            a.sort = form.cleaned_data['sort']        
            a.save()
                        
            url = reverse('community-display', kwargs={'community':community})
            return HttpResponseRedirect(url)
    else:
        data = {
            'name':a.name,
            'description':a.description,
            'sort': a.sort
        }
        form = AreaForm(initial=data)

    context = {'form': form, 'community_obj':c, 'area_obj':a}
    return render(request, context)  

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def list(request, community, render):
    c = Community.objects.get(key_name=community)
    context = {'community':c}
    return render(request, context)
