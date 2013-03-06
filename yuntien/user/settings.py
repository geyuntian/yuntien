# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.community.common.settings import *

USER_ID_REGEX = r'[a-z][a-z0-9_]{3,19}'
USER_PREFIX = 'user'
RESERVED_USER_IDS = (u'me', u'admin')

DEFAULT_USER_WIDGETS = {
                        
'blog': {
'id':'blog',
'sort':10,
'name':u'博客',
'app_id':'note',
}, 
                        
}
USER_WIDGETS = getattr(settings, 'YT_USER_WIDGETS', DEFAULT_USER_WIDGETS)

DEFAULT_USER_PROFILE_IMAGE = getattr(settings, 'YT_DEFAULT_USER_PROFILE_IMAGE', '')
