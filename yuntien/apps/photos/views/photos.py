from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from django import forms
from django.core.paginator import Paginator
from yuntien.common.db import *
from yuntien.authext.views.decorators import *
from yuntien.authext.models.auth import *
from yuntien.base.views.decorators.db import *
from yuntien.base.views.request import get_int_param, check_request_method
from yuntien.community.common.settings import WIDGET_ID_REGEX
from yuntien.base.models.image import *
from yuntien.community.main.models.community import Community, Widget
from yuntien.community.main.settings import COMMUNITY_REGEX, APPS
from yuntien.apps.photos.models.photo import Photo, SOURCE_TYPE_COMMUNITY

class PhotoForm(forms.Form):
    title = forms.CharField(required=True, max_length=140)
    photo = forms.ImageField(required=True)

def _find_widget(cls, request, *args, **kwds):
    if kwds.has_key('community') and kwds.has_key('widget'):
        c = Community.objects.get(key_name=kwds['community'])
        return c.widget_set.get(key_name=kwds['widget'])

@check_authorization(Widget, OPERATION_POST, finder=_find_widget)
def add(request, community, widget, render):
    
    community_obj = Community.objects.get(key_name=community)
    widget_config = community_obj.widget_set.get(key_name=widget)
        
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(user=request.user)
            photo.title = form.cleaned_data['title']
            photo.source_type = SOURCE_TYPE_COMMUNITY
            photo.source_id = community_obj.id
            photo.source_widget_id = widget_config.id
            photo.save()
            
            photo_file = request.FILES['photo']
            photo_name, photo_ext = os.path.splitext(photo_file.name)
            
            #save original file
#            original = u'original/photos/%d%s' % (photo.id, photo_ext)
#            handler1 = ImageHandler(original)

            thumbnail = u'thumbnail/photos/%d.jpg' % photo.id
            handler2 = SquareImageHandler(thumbnail, 180) 

            large = u'large/photos/%d.jpg' % photo.id
            handler3 = FixedWidthImageHandler(large, 800, 1600) 

            medium = u'medium/photos/%d.jpg' % photo.id
            handler4 = FixedWidthImageHandler(medium, 180, 600)

            photo.save_image(photo_file, (handler2, handler3, handler4))            
            
            url = reverse('community-widget', kwargs={'community':community, 'widget':widget})
            return HttpResponseRedirect(url)      
    else:
        form = PhotoForm() # An unbound form

    context = {'form': form, 'community_obj': community_obj, 'widget_config': widget_config}
    return render(request, context)

def list(request, community, widget, render, num_per_page=10):
    community_obj = Community.objects.get(key_name=community)
    widget_config = community_obj.widget_set.get(key_name=widget)
    
    filters = []
    filters.append(lambda q: q.filter(source_type=SOURCE_TYPE_COMMUNITY))    
    filters.append(lambda q: q.filter(source_widget_id=widget_config.id))    
    photos = build_query(Photo, filters)
    p = Paginator(photos, num_per_page)
    page = p.page(get_int_param(request, 'page', 1))
    photos = page.object_list

    context = {'photos': photos, 
               'page_info': page,
               'community_obj': community_obj, 
               'widget_config': widget_config}
    return render(request, context)

@check_id(Photo)
def show(request, community, widget, id, render):
    photo = Photo.objects.get(pk=id)
    context = {'photo': photo,
               'community_obj': photo.source, 
               'widget_config': photo.source_widget}
    return render(request, context)

@check_request_method(methods=('POST'))
@check_id(Photo)
@check_authorization(Photo, OPERATION_DELETE)
def delete(request, community, widget, id):
    photo = Photo.objects.get(pk=id)
    photo.delete()
    return HttpResponse('Deleted!')        
