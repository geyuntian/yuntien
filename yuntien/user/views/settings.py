# -*- coding:utf-8 -*-
import copy, os
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from yuntien.authext.views.decorators import check_authorization, check_user
from yuntien.base.models.image import *

class PhotoForm(forms.Form):
    photo = forms.ImageField(required=True)

@check_user()
def set_photo(request, render):
    user_obj = request.user
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = request.FILES['photo']
            photo_name, photo_ext = os.path.splitext(photo.name)
            
            #save original file
            original = u'original/user/%d%s' % (user_obj.id, photo_ext)
            handler1 = ImageHandler(original)
            icon = u'icon/user/%d.jpg' % user_obj.id
            handler2 = SquareImageHandler(icon, 50)        
            user_obj.save_image(photo, (handler1, handler2))
            
            user_obj.has_profile_image = True
            user_obj.save()
            
            url = reverse('user-display', kwargs={'user':user_obj.username})
            return HttpResponseRedirect(url)

    else:
        form = PhotoForm() # An unbound form

    context = {'form': form, 'user_obj':user_obj}
    return render(request, context)    
