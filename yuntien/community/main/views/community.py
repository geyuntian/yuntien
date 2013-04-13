# -*- coding:utf-8 -*-
import copy
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from yuntien.common.markup import text_markup
from yuntien.common.db import *
from yuntien.common.http import HttpResponseDirectOutput, HttpResponseRichOutput
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.authext.models.auth import ROLE_OWNER, ROLE_USER, OPERATION_EDIT
from yuntien.base.views.decorators.db import check_name
from yuntien.base.views.request import check_request_method, get_int_param
from yuntien.community.main.models.community import Community, Tag, STYLE_SIMPLE, STYLE_TAB
from yuntien.community.main.settings import RESERVED_COMMUNITY_IDS
from yuntien.community.main.settings import APPS, COMMUNITY_REGEX
from yuntien.community.main.validators import validate_community
from yuntien.community.main.views.tool import render_404

def _find_community(cls, request, *args, **kwds):
    if kwds.has_key('community'):
        return Community.objects.get(key_name=kwds['community'])

def _validate_community(value):
    if value in RESERVED_COMMUNITY_IDS:
        raise ValidationError(_(u'%s is a reserved community id.') % value)
    try:
        Community.objects.get(key_name=value)
        raise ValidationError(_(u'%s already exists.') % value)
    except Community.DoesNotExist:
        pass

@permission_required('main.add_community')
def add(request, render):
    
    class CommunityForm(forms.Form):
        id = forms.RegexField(regex='^'+COMMUNITY_REGEX+'$', required=True, max_length=100, validators=[_validate_community])
        name = forms.CharField(required=True, max_length=20)
        description = forms.CharField(required=False, widget=forms.Textarea)
        tags = forms.CharField(required=False, max_length=100)
    
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['id']

            community = Community(key_name=c)
            community.name = form.cleaned_data['name']
            community.description = text_markup.render( form.cleaned_data['description'] )
            community.raw_description = form.cleaned_data['description']
            community.add_tags( form.cleaned_data['tags'] )
            community.created_by = request.user
            community.save()
            
            url = reverse(display, kwargs={'community':c})
            return HttpResponseRedirect(url)
    else:
        form = CommunityForm() # An unbound form

    context = {'form': form, 'user':request.user}
    return render(request, context)

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def edit(request, community, render):
    c = Community.objects.get(key_name=community)
    
    def _validate_users(value):
        users = value.splitlines()
        users = [u for u in users if u]
        if len(users) > 10:
            raise ValidationError(_(u'Too many users.'))
        for u in users:
            user = None
            try:
                user = get_user_model().objects.get(username=u)
            except:
                raise ValidationError(_(u'%s is not a valid user.') % u)
            role = c.get_role(user)
            if role not in (ROLE_OWNER, ROLE_USER):
                raise ValidationError(_(u"%s hasn't joined this community yet.") % u)
    
    class CommunityForm(forms.Form):
        name = forms.CharField(required=True, max_length=20)
        description = forms.CharField(required=False, widget=forms.Textarea)
        admins = forms.CharField(required=False, widget=forms.Textarea, validators=[_validate_users])
        tags = forms.CharField(required=False, max_length=100)
        style = forms.TypedChoiceField(required=True, choices=[(STYLE_SIMPLE, _(u"Simple")), (STYLE_TAB, _(u"Tab"))], coerce=int)

    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            c.name = form.cleaned_data['name']
            c.description = text_markup.render( form.cleaned_data['description'] )
            c.raw_description = form.cleaned_data['description']
            c.add_tags( form.cleaned_data['tags'] )      
            c.style = form.cleaned_data['style']   

            users = form.cleaned_data['admins'].splitlines()
            users = [u for u in users if u]
            c.set_admins(users)
            
            c.save()
                        
            url = reverse(display, kwargs={'community':community})
            return HttpResponseRedirect(url)
    else:
        admins = [ra.user.username for ra in c.ra_set.filter(role=ROLE_OWNER)]
        
        data = {
            'id':c.key_name,
            'name':c.name,
            'description':c.raw_description,
            'admins':'\n'.join(admins),
            'tags': c.get_tag_str(),
            'style': c.style,
        }
        form = CommunityForm(data)

    context = {'form':form, 'community':c}
    return render(request, context) 

@check_name(Community, name='community')
def display(request, community, render, area=''):
    c = Community.objects.get(key_name=community)
    
    areas = c.area_set.all()[:10]
    if not area and areas:
        area = areas[0].key_name
        
    area_obj = None
    for a in areas:
        if a.key_name == area:
            area_obj = a
    
    if area and c.style == STYLE_TAB:
        widgets = c.widget_set.filter(area=area_obj)
    else:        
        widgets = c.widget_set.all()
    path = reverse('community-display', kwargs={'community':community})
    
    for w in widgets:
        view, args, kwargs = resolve(path, w.app_config['urls'])
        kwargs['widget'] = w.key_name
        response = view(request, *args, **kwargs)
        w.content = response.content
        
    context = {
        'community':c,
        'area':area,
        'areas':areas,
        'widgets':widgets,
    }
    return render(request, context)

@check_name(Community, name='community')
def dispatch(request, render, community, widget, path=''):
    c = Community.objects.get(key_name=community)
    w = c.widget_set.get(key_name=widget)
    
    if not w:
        return render_404(request)
    
    title = ''
    head = ''
    sidebar = ''
    
    view, args, kwargs = resolve(request.path, w.app_config['urls'])
    kwargs['community'] = community
    kwargs['widget'] = widget
    response = view(request, *args, **kwargs)
    if isinstance(response, HttpResponseRedirect):
        return response
    elif isinstance(response, HttpResponseDirectOutput):
        return response
    elif isinstance(response, HttpResponseRichOutput):
        w.content = response.content
        title = response.get_title()
        head = response.get_head()
        sidebar = response.get_sidebar()
    else:
        w.content = response.content
        
    context = {
        'title':title,
        'head':head,
        'sidebar':sidebar,
        'community':c,
        'area':w.area.key_name,
        'areas':c.area_set.all(),
        'widget':w
    }
    return render(request, context)

def list_by_tags(request, render, num_per_page=10):
    tags = Tag.objects.all()[:num_per_page]
    
    for tag in tags:
        tag.communities = Community.objects.filter(tags__name=tag.name)[:32]
        
    my_communities = []
    if request.user.is_authenticated():
        my_communities = [ra.obj for ra in request.user.main_ra_set.all()[:32]]
    
    context = {
        'my_communities': my_communities,
        'tags': tags,
#        'page_info': page,
    }
    return render(request, context)

def _all(request, render, filters=[], num_per_page=20):
    communities = build_query(Community, filters)    
    p = Paginator(communities, num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    
    context = {
        'communities': page.object_list ,
        'page_info': page,
    }
    return render(request, context)

def all(request, render, num_per_page=20):
    filters = []
    if request.GET.has_key('tag'):
        filters.append(lambda q: q.filter(tags__name=request.GET['tag']))

    return _all(request, render, filters, num_per_page)

#def latest(request, render, num_per_page=20):
#    filters = []
#    filters.append(lambda q: q.order('-time'))
#    return _all(request, render, filters, num_per_page)

@check_user()
@check_request_method(methods=('POST'))
@check_name(Community, name='community')
def join(request, community):
    c = Community.objects.get(key_name=community)
    c.join(request.user)
    return HttpResponse('Joined!')

@check_user()
@check_request_method(methods=('POST'))
@check_name(Community, name='community')
def leave(request, community):
    c = Community.objects.get(key_name=community)
    c.leave(request.user)
    return HttpResponse('Left!')
