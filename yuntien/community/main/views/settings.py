# -*- coding:utf-8 -*-
import copy, os
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import File, ContentFile
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from yuntien.authext.views.decorators import check_authorization
from yuntien.authext.models.auth import OPERATION_EDIT
from yuntien.base.views.decorators.db import check_name
from yuntien.base.models.image import *
from yuntien.community.main.models.community import Community

def _find_community(cls, request, *args, **kwds):
    if kwds.has_key('community'):
        return Community.objects.get(key_name=kwds['community'])

class PhotoForm(forms.Form):
    photo = forms.ImageField(required=True)

@check_name(Community, name='community')
@check_authorization(Community, OPERATION_EDIT, finder=_find_community)
def set_logo(request, community, render):
    community_obj = Community.objects.get(key_name=community)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = request.FILES['photo']
            photo_name, photo_ext = os.path.splitext(photo.name)

            #save original file
            original = u'original/community/%d%s' % (community_obj.id, photo_ext)
            handler1 = ImageHandler(original)
            icon = u'icon/community/%d.jpg' % community_obj.id
            handler2 = SquareImageHandler(icon, 50)        
            community_obj.save_image(photo, (handler1, handler2))
            
            community_obj.has_logo_image = True
            community_obj.save()
           
            url = reverse('community-display', kwargs={'community':community})
            return HttpResponseRedirect(url)

    else:
        form = PhotoForm() # An unbound form

    context = {'form': form, 'community':community_obj}
    return render(request, context)    
