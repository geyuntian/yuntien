# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import *
from django.http import *
from django.utils import feedgenerator
from django.utils.simplejson import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.authext.models.auth import *
from yuntien.base.views.decorators.db import *
from yuntien.base.views.request import get_int_param
from yuntien.base.models.post import *
from yuntien.base.models.tag import *
from yuntien.common.db import *
from yuntien.apps.tui.models import Topic, Comment, Domain
from yuntien.apps.tui.settings import CONFIG
from yuntien.community.main.models.community import Community, Widget
from yuntien.community.main.validators import validate_community
from yuntien.community.main.settings import COMMUNITY_REGEX, APPS
from tool import render_404, render_json

ORDER = {
    'new': '-date',
    'old': 'date',
    'hot': '-up_down_count',
    'best': '-quality',
    'top': '-points',
    'controversial': 'up_down_ratio',
}

def _validate_community(value):
    try:
        c = Community.objects.get(key_name=value)
        c.widget_set.get(app='tui')
    except:
        raise ValidationError(_(u'%s is not a valid community.') % value)

class TuiForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    category = forms.RegexField(regex=COMMUNITY_REGEX+'$', required=True, max_length=100, validators=[_validate_community])
    link = forms.URLField(required=True, max_length=250)
    sync = forms.BooleanField(required=False, initial=True)
    
class CommentForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)      

@check_authorization(Topic, OPERATION_ADD, view=render_404)
def add(request, render):
    if request.method == 'POST':
        form = TuiForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['category']
            community = Community.objects.get(key_name=c)
            community_widget = community.widget_set.get(key_name='tui')
            post = Topic(community=community, community_widget=community_widget, author=request.user)
            post.title = form.cleaned_data['title']
            post.link = form.cleaned_data['link']
            post.save()
            
            url = reverse(display, kwargs={'id':str(post.id)})

            return HttpResponseRedirect(url)
    else:
        form = TuiForm(initial={'category': request.GET.get('category', '')}) # An unbound form

    context = {'form': form, 'user_obj':request.user}
    return render(request, context)

def _find_widget(cls, request, *args, **kwds):
    if kwds.has_key('community') and kwds.has_key('widget'):
        c = Community.objects.get(key_name=kwds['community'])
        return c.widget_set.get(key_name=kwds['widget'])

@check_authorization(Widget, OPERATION_POST, finder=_find_widget)  
def add_in_widget(request, community, widget, render):
    
    community_obj = Community.objects.get(key_name=community)
    widget_config = community_obj.widget_set.get(key_name=widget)
    
    class _TuiForm(forms.Form):
        title = forms.CharField(required=True, max_length=100)
        link = forms.URLField(required=True, max_length=250)
    
    if request.method == 'POST':
        form = _TuiForm(request.POST)
        if form.is_valid():
            post = Topic(community=community_obj, community_widget=widget_config, author=request.user)
            post.title = form.cleaned_data['title']
            post.link = form.cleaned_data['link']
            post.save()
            
            url = reverse(display, kwargs={'id':str(post.id)})

            return HttpResponseRedirect(url)
    else:
        form = _TuiForm() # An unbound form

    context = {'form': form, 
               'community_obj': community_obj, 
               'widget_config': widget_config, 
               'user_obj':request.user}
    return render(request, context)

def _list(request, render, num_per_page=10, filters=[], c={}, community='', widget='', home=False):
    filters = filters #get_common_filters(request) + filters

    if community and widget:
        w = Community.objects.get(key_name=community).widget_set.get(key_name=widget)
        filters.append(lambda q: q.filter(community_widget=w))
        
        if home:
            num_per_page = w.num_on_homepage
        else:
            num_per_page = w.num_per_page
    
    posts = build_query(Topic, filters)    
    p = Paginator(posts, num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    posts = page.object_list

    community_obj = None
    if community:
        community_obj = Community.objects.get(key_name=community)
    widget_config = None
    if widget:
        widget_config = community_obj.widget_set.get(key_name=widget)
            
    context = {
        'posts': posts,
        'page_info': page,
        'community': community,
        'community_obj': community_obj,
        'widget': widget,
        'widget_config': widget_config,
        'app_config': APPS.get('tui', None)
    }
    context.update(c)
    return render(request, context)

def list(request, render, num_per_page=10, c={}, community='', widget='', home=False):
    filters = []
#    if community:
#        filters.append(lambda q: q.filter('category =', community))
    return _list(request, render, num_per_page, filters, c, community, widget, home)

def list_by_domain(request, domain, render):
    filters = []
    try:
        d = Domain.objects.get(domain_name=domain)
        filters.append(lambda q: q.filter(domain=d))
    except:
        raise Http404
    return _list(request, render, 10, filters, {'domain':domain})

def list_by_user_id(request, user, render, num_per_page=10):
    filters = []
    u = User.objects.get(username=user)
    filters.append(lambda q: q.filter(author=u))
    return _list(request, render, num_per_page, filters, {'author':u})

@check_id(Topic)
def display(request, id, render, community='', widget=''):
    filters = []
    post = Topic.objects.get(id=id)

    page_info = None
    comments = post.comment_set.all()
    for c in comments:
        c.request = request
    if _get_sort_parameter(request) == 'list':
        comments = [_fill_comment(c) for c in comments]
        for c in comments:
            c.display_level = 1
    else:        
        comments = [_fill_comment(c) for c in comments]
        for c in comments:
            c.display_level = 1        
        
    post.comments = comments
        
    context = {
        'post':_fill_post(post),
        'community':post.community,
#        'comments':comments,
        'page_info':page_info,
        'form':CommentForm()
    }
    return render(request, context)

@check_id(Comment)
def display_comment(request, id, render):
    comment = Comment.objects.get(id=id)
    comment.is_current = True
    comment.request = request
    comment = _fill_comment(comment)
    comment.display_level = 1
    
    comments = []
    pages = 0
    versions = []
    
    context = {
        'post':_fill_post(comment.topic),
        'community':comment.community,
        'current_comment':comment,
        'sort':_get_sort_parameter(request),
        'comments':[comment],
        'versions': versions,
        'pages':pages,
        'current_page':get_int_param(request, 'page', 0),
        'form':CommentForm()
    }
    return render(request, context)

def list_comments(request, render, num_per_page=10, filters=[], c={}):
    
    comments = build_query(Comment, filters)    
    p = Paginator(comments, num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    comments = page.object_list  
    comments = [_fill_comment(comment, comment.level) for comment in comments]
    for comment in comments:
        comment.request = request
        comment.display_level = 1    
    
    context = {
        'comments': comments,
        'page_info': page,
    }
    context.update(c)
    return render(request, context)

def list_latest_comments(request, render, num_per_page=10):
    filters = []
#    filters.append(lambda q: q.order('-date'))    
    return list_comments(request, render, num_per_page, filters)
    
@check_id(Topic)
@check_authorization(Topic, OPERATION_DELETE, view=render_404)
def delete(request, id):
    if request.method == 'POST':
        tui = Topic.objects.get(id=id)
        tui.delete(check_children=True)
        return HttpResponse('Done!')
    return render_404()

@check_id(Topic)
@check_user()
def up(request, id):
    if request.method == 'POST':
        tui = Topic.objects.get(id=id)
        tui.vote_up(request.user)
        return HttpResponse('Done!')
    return render_404()

@check_id(Topic)
@check_user()
def down(request, id):
    if request.method == 'POST':
        tui = Topic.objects.get(id=id)
        tui.vote_down(request.user)
        return HttpResponse('Done!')
    return render_404()

def _fill_post(post):
    return post

def _fill_comment(comment, top_level=0):
    comment.display_level = comment.level - top_level + 1
    comment.form = CommentForm({'content':comment.raw_content})
    if comment.display_level > 10:
        return comment
    if hasattr(comment, 'comments'):
        for c in comment.comments:
            _fill_comment(c, top_level)
            c.request = comment.request
    return comment

def _get_sort_parameter(request):
    order = ''
    if request.GET.has_key('sort'):
        order = request.GET['sort']
    return order

def _get_order(request):
    order = ''
    if request.GET.has_key('sort'):
        order = request.GET['sort']
    return _get_order_filter(order)

def _get_order_filter(order):    
    order_str = '-date'
    if order in ORDER:
        order_str = ORDER[order]
    return lambda q: q.order(order_str)

def render_tui(request, context):
    c = {}
    c['posts'] = []
    for t in context['posts']:
        tui = {}
        tui['title'] = t.title
        tui['link'] = t.link
        c['posts'].append(tui)
    return render_json(request, c)

def render_feed(request, context, title=CONFIG['site_title'], descr=CONFIG['site_description']):
    if 'category' in context:
        title = context['category'] + ' - ' + title
    if 'domain' in context:
        title = context['domain'] + ' - ' + title
    if 'author' in context:
        title = context['author'].username + ' - ' + title
    
    f = feedgenerator.Rss201rev2Feed(
        title=title, 
        link=request.host_url, 
        description=descr,
        feed_url=request.build_absolute_uri(request.host_url))

    for post in context['posts']:
        content = post.content or '<a href="%s">%s</a>' % (post.link, post.title)
        f.add_item(
            title=post.title, 
            link=request.host_url+reverse(display, kwargs={'id':str(post.id)}), 
            description=content,
            author_name=post.author.username,
            pubdate=post.date_time)
        
    return HttpResponse(f.writeString('UTF-8') , mimetype="application/rss+xml")
