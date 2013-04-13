# -*- coding:utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import *
from django.contrib.auth import get_user_model
from yuntien.common.exceptions import YTError
from yuntien.base.views.request import check_request_method, get_int_param
from yuntien.authext.views.decorators import check_authorization, check_user

@check_user()
@check_request_method(methods=('POST'))
def create(request, user, friend):
    f = get_user_model().objects.get(username=friend)
    request.user.create_friendship(f)
    return HttpResponse('Followed!')

@check_user()
@check_request_method(methods=('POST'))
def destroy(request, user, friend):
    f = get_user_model().objects.get(username=friend)
    request.user.destroy_friendship(f)
    return HttpResponse('Unfollowed!')
