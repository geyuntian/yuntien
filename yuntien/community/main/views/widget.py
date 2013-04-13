# -*- coding:utf-8 -*-
import copy
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from yuntien.authext.views.decorators import check_admin, check_authorization
from yuntien.authext.models.auth import OPERATION_EDIT
from yuntien.base.views.decorators.db import check_name
from yuntien.common.markup import text_markup
from yuntien.framework.models import widget
from yuntien.app.models.app import App
from yuntien.community.main.models.community import Community, Widget
from yuntien.community.common.settings import WIDGET_ID_REGEX, RESERVED_WIDGET_IDS
from yuntien.community.main.settings import APPS, COMMUNITY_REGEX

def _find_community(cls, request, *args, **kwds):
    if kwds.has_key('community'):
        return Community.objects.get(key_name=kwds['community'])   
    
PRIVACY_TYPE_CHOICES = [(widget.PUBLIC, _(u"Everyone can submit content")),
                        (widget.MEMBER_ONLY, _(u"Only member can submit content")),
                        (widget.OWNER_ONLY, _(u"Only admin can submit content"))]
        
@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def add(request, community, render):
    c = Community.objects.get(key_name=community)

    def _validate_widget_id(value):
        if value in RESERVED_WIDGET_IDS:
            raise ValidationError(_(u'%s is a reserved widget id.') % value)
        if value:
            try:
                c.widget_set.get(key_name=value)
                raise ValidationError(_(u'%s is already used.') % value)
            except Widget.DoesNotExist:
                pass
    
    def _validate_app_id(value):
        app = APPS.get(value)
        if not app:
            raise ValidationError(_(u'%s is not a valid app.') % app)
        if not app['multiple_widgets'] and c.get_widgets(value):
            raise ValidationError(_(u'%s is already used.') % app['name'])

    class WidgetForm(forms.Form):
        widget_id = forms.RegexField(regex='^'+WIDGET_ID_REGEX+'$', required=True, validators=[_validate_widget_id])
        app_id = forms.ModelChoiceField(required=True, queryset=App.objects.all(), empty_label=None)
        area_id = forms.ChoiceField(required=True, choices=[(area.key_name, area.name) for area in c.area_set.all()])
        name = forms.CharField(required=True, max_length=20)
        description = forms.CharField(required=False, widget=forms.Textarea)
        sort = forms.IntegerField(required=True, initial=0) 
        privacy_type = forms.TypedChoiceField(required=True, choices=PRIVACY_TYPE_CHOICES, coerce=int)       
    
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            widget = Widget(key_name=form.cleaned_data['widget_id'], app=form.cleaned_data['app_id'], name=form.cleaned_data['name'])
            widget.area = c.area_set.get(key_name=form.cleaned_data['area_id'])
            widget.community = c
            widget.description = text_markup.render( form.cleaned_data['description'] )
            widget.raw_description = form.cleaned_data['description']
            widget.sort = form.cleaned_data['sort']
            widget.privacy_type = form.cleaned_data['privacy_type']
            widget.save()
            
            url = reverse('community-display', kwargs={'community':community})
            return HttpResponseRedirect(url)
    else:
        form = WidgetForm() # An unbound form

    context = {'form': form, 'community_obj':c}
    return render(request, context)

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def edit(request, community, widget, render):
    c = Community.objects.get(key_name=community)
    w = c.widget_set.get(key_name=widget)
    
    class WidgetForm(forms.Form):
        area_id = forms.ChoiceField(required=True, choices=[(area.key_name, area.name) for area in c.area_set.all()])
        name = forms.CharField(required=True, max_length=20)
        description = forms.CharField(required=False, widget=forms.Textarea)
        sort = forms.IntegerField(required=True, initial=0)
        privacy_type = forms.TypedChoiceField(required=True, choices=PRIVACY_TYPE_CHOICES, coerce=int)       

    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            w.area = c.area_set.get(key_name=form.cleaned_data['area_id'])
            w.name = form.cleaned_data['name']
            w.description = text_markup.render( form.cleaned_data['description'] )
            w.raw_description = form.cleaned_data['description']
            w.sort = form.cleaned_data['sort']   
            w.privacy_type = form.cleaned_data['privacy_type']     
            w.save()
                        
            url = reverse('community-display', kwargs={'community':community})
            return HttpResponseRedirect(url)
    else:
        data = {
            'area_id':w.area.key_name,
            'name':w.name,
            'description':w.raw_description,
            'sort':w.sort,
            'privacy_type':w.privacy_type
        }
        form = WidgetForm(initial=data)

    context = {'form': form, 'community_obj':c, 'widget_obj':w}
    return render(request, context)  

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def list(request, community, render):
    c = Community.objects.get(key_name=community)
    context = {'community':c}
    return render(request, context)
