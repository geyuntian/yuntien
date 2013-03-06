# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.base.views.plugin import *

_CONFIG = {}
_CONFIG['site_title'] = u'Site Title'
_CONFIG['site_description'] = u'site description...'

CONFIG = getattr(settings, 'YT_FORUM_CONFIG', _CONFIG)

APP_ID = getattr(settings, 'YT_PHOTOS_APP_ID', 'photos')

PLUGINS = getattr(settings, 'YT_PHOTOS_PLUGINS', ())
