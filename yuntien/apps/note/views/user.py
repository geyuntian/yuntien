from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.utils import feedgenerator
from django.utils.simplejson import *
from django import forms
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.authext.models.user import get_current_user
from yuntien.authext.models.auth import *
from yuntien.base.views.decorators.db import check_name, check_id
from yuntien.base.views.request import get_int_param
from yuntien.base.models.post import *
from yuntien.base.models.tag import *
from yuntien.common.db import *
from yuntien.community.common.settings import WIDGET_ID_REGEX
from yuntien.community.main.models.community import Community
from yuntien.community.main.settings import COMMUNITY_REGEX, APPS
from yuntien.user.models import Widget
from yuntien.apps.note.context import *
from yuntien.apps.note.models import Topic, Comment
from yuntien.common.markup import text_markup

def _get_user(request, *args, **kwds):
    u = request.user
    if u:
        return u.username == kwds.get('user', '')
    return False

@check_user(func=_get_user)
def add(request, user, widget, render):
    
    class PostForm(forms.Form):
        title = forms.CharField(max_length=100)
        tags = forms.CharField(required=False, max_length=100)
        content = forms.CharField(required=False, widget=forms.Textarea)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Topic()
            post.author = get_current_user()
            post.title = form.cleaned_data['title']
            post.content = text_markup.render( form.cleaned_data['content'] )
            post.raw_content = form.cleaned_data['content']
            post.add_tags( form.cleaned_data['tags'] )
            post.user = get_current_user()
            post.user_widget = post.author.user_widget_set.get(key_name=widget)
            post.save()
            kwargs={
                    'user':user,
                    'widget':widget,
                    'id':str(post.id)}
            redirect = reverse('note-user-topic', urlconf=APPS['note']['urls'], kwargs=kwargs)
            return HttpResponseRedirect(redirect)
    else:
        form = PostForm(initial={}) # An unbound form

    context = {'form': form, 'user':user, 'widget':widget}
    return render(request, context)

@check_id(Topic)
@check_authorization(Topic, OPERATION_EDIT)
def edit(request, user, widget, id, render):
    
    widget_config = request.user.user_widget_set.get(key_name=widget)
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
            params = {'id':str(post.id), 'user':user, 'widget':widget}
            redirect = reverse('note-user-topic', urlconf=APPS[APP_ID]['urls'], kwargs=params)
            return HttpResponseRedirect(redirect)
    else:
        data = {
            'title':post.title,
            'tags':post.get_tag_str(),
            'content':post.raw_content,
        }
        form = PostForm(initial=data)

    context = {'form':form, 'post':post, 'widget_config': widget_config}
    return render(request, context) 

@check_id(Topic)
@check_authorization(Topic, OPERATION_DELETE)
def delete(request, user, widget, id):
    if request.method == 'POST':
        post = Topic.objects.get(pk=id)
        post.delete()
        return HttpResponse('Deleted!')
    return HttpResponseNotFound()

def get_common_filters(request):
    filters = []
    
    if request.GET.has_key('tag'):
        filters.append(lambda q: q.filter(tags__name=request.GET['tag']))
        
    return filters

def _list(request, render, num_per_page=10, filters=[], user='', widget='', c={}):
    filters = get_common_filters(request) + filters
    u = get_user_model().objects.get(username=user)

    w = u.user_widget_set.get(key_name=widget)
    filters.append(lambda q: q.filter(user_widget=w))
    
    posts = build_query(Topic, filters)    
    p = Paginator(posts, num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    posts = page.object_list
            
    context = {
        'posts': posts,
        'page_info': page,
        'user_obj': u,
        'widget': widget,
        'widget_config': w,
        'app_config': APPS.get('note', None),   
    }
    context.update(c)
    return render(request, context)

def list_by_user_id(request, render, user, widget='blog', num_per_page=10):
    return _list(request, render, num_per_page, [], user=user, widget=widget)
