from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.utils import feedgenerator
from django.template import RequestContext 
from django.utils.simplejson import *
from django import forms
from django.core.paginator import Paginator
from yuntien.authext.views.decorators import check_authorization
from yuntien.authext.models.auth import *
from yuntien.base.views.decorators.db import *
from yuntien.base.views.request import get_int_param
from yuntien.base.models.post import *
from yuntien.base.models.tag import *
from yuntien.common.db import *
from yuntien.common.http import HttpResponseDirectOutput
#from yuntien.community.common.helpers.validators import validate_community
from yuntien.community.common.settings import WIDGET_ID_REGEX
from yuntien.community.main.models.community import Community, Widget
from yuntien.community.main.settings import COMMUNITY_REGEX, APPS
from yuntien.apps.note.settings import NUM_PER_PAGE, CONFIG, TAG_LIMIT, APP_ID
from yuntien.apps.note.context import *
from yuntien.apps.note.models import Topic, Comment
from yuntien.common.markup import text_markup

class CommentForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)  
    
def _find_community(cls, request, *args, **kwds):
    if request.REQUEST.get('community', ''):
        return cls.objects.get(key_name=request.REQUEST.get('category', ''))
    
def _find_widget(cls, request, *args, **kwds):
    if kwds.has_key('community') and kwds.has_key('widget'):
        c = Community.objects.get(key_name=kwds['community'])
        return c.widget_set.get(key_name=kwds['widget'])

@check_authorization(Widget, OPERATION_POST, finder=_find_widget)    
def add(request, community, widget, render):
    
    community_obj = Community.objects.get(key_name=community)
    widget_config = community_obj.widget_set.get(key_name=widget)
    
    class PostForm(forms.Form):
        title = forms.CharField(max_length=100)
        tags = forms.CharField(required=False, max_length=100)
        content = forms.CharField(required=False, widget=forms.Textarea)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Topic(author=request.user)
            post.title = form.cleaned_data['title']
            post.content = text_markup.render( form.cleaned_data['content'] )
            post.raw_content = form.cleaned_data['content']
            post.add_tags( form.cleaned_data['tags'] )
            post.community = community_obj
            post.community_widget = widget_config
            post.save()
            params = {'id':str(post.id), 'community':community, 'widget':widget}
            redirect = reverse(display, urlconf=APPS[APP_ID]['urls'], kwargs=params)
            return HttpResponseRedirect(redirect)
    else:
        form = PostForm() # An unbound form

    context = {'form': form, 'community_obj': community_obj, 'widget_config': widget_config}
    return render(request, context)    

@check_id(Topic)
@check_authorization(Topic, OPERATION_EDIT)
def edit(request, community, widget, id, render):
    
    community_obj = Community.objects.get(key_name=community)
    widget_config = community_obj.widget_set.get(key_name=widget)
    post = Topic.objects.get(pk=id)
    
    class PostForm(forms.Form):
        title = forms.CharField(max_length=100)
        tags = forms.CharField(required=False, max_length=100)
        content = forms.CharField(required=False, widget=forms.Textarea)    
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = text_markup.render( form.cleaned_data['content'] )
            post.raw_content = form.cleaned_data['content']
            post.add_tags( form.cleaned_data['tags'] )
            post.save()
            params = {'id':str(post.id), 'community':community, 'widget':widget}
            redirect = reverse(display, urlconf=APPS[APP_ID]['urls'], kwargs=params)
            return HttpResponseRedirect(redirect)
    else:
        data = {
            'title':post.title,
            'tags':post.get_tag_str(),
            'content':post.raw_content,
        }
        form = PostForm(initial=data)

    context = {'form':form, 'post':post, 'community_obj': community_obj, 'widget_config': widget_config}
    return render(request, context)    
    
@check_id(Topic)
@check_authorization(Topic, OPERATION_DELETE)
def delete(request, community, widget, id):
    if request.method == 'POST':
        post = Topic.objects.get(pk=id)
        post.delete()
        return HttpResponse('Deleted!')
    return HttpResponseNotFound()

def _list(request, render, num_per_page=10, filters=[], community='', widget='', c={}):
    filters = get_common_filters(request) + filters

    if community and widget:
        w = Community.objects.get(key_name=community).widget_set.get(key_name=widget)
        filters.append(lambda q: q.filter(community_widget=w))
    
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
        'app_config': APPS.get('note', None),   
    }
    context.update(c)
    return render(request, context)

def get_common_filters(request):
    filters = []
    
    if request.GET.has_key('tag'):
        filters.append(lambda q: q.filter(tags__name=request.GET['tag']))
        
    return filters

def list(request, render, num_per_page=10, community='', widget=''):
    filters = []
    return _list(request, render, num_per_page, filters, community, widget)

@check_id(Topic)
def display(request, id, render, community='', widget='', user=''):
    post = Topic.objects.get(pk=id)
    
#    filters = []
#    filters.append(lambda q: q.filter('ref =', post))
#    filters.append(lambda q: q.order('date'))
#    
#    comments, page = Paginator(request, YTNoteComment, filters, 10).get_page_objects()
    
    context = {
        'title': post.title,
        'post':post,
        'community': post.community,
#        'comments': comments,
#        'page_info': page,
        'form':CommentForm()
    }
    return render(request, context)  

def render_feed(request, context, title=CONFIG['site_title'], descr=CONFIG['site_description']):
    if request.GET.has_key('tag'):
        title = request.GET.get('tag', '') + ' - ' + title  
        
    community = context.get('community_obj', None)
    widget = context.get('widget_config', None)
    if community and widget:
        title = widget.name + ' - ' + community.name
        descr = ''
    
    f = feedgenerator.Rss201rev2Feed(title=title, link=request.host_url, description=descr,
                                     feed_url=request.build_absolute_uri(request.host_url))
    for post in context['posts']:
        f.add_item(
            title=post.title, 
            link=request.host_url+_get_url(post), 
            description=post.content,
            author_name=post.author.username,
            pubdate=post.date_time)
        
    return HttpResponseDirectOutput(f.writeString('UTF-8') , mimetype="application/rss+xml")

def _get_url(post):
    urls = APPS['note']['urls']
    
    try:
        if post.community:
            kwargs = {'id':post.id, 'community':post.community.key_name, 'widget':post.community_widget.key_name}
            return reverse('note-topic', urlconf=urls, kwargs=kwargs)
        else:
            kwargs = {'id':post.id, 'user':post.user.username, 'widget':post.user_widget.key_name}
            return reverse('note-user-topic', urlconf=urls, kwargs=kwargs)
    except:
        return ''
