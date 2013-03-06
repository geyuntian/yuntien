# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.community.common.settings import *

COMMUNITY_PREFIX = 'community'

TEMPLATE_404 = getattr(settings, 'YT_MAIN_TEMPLATE_404', None) or 'main/404.html'
TEMPLATE_MESSAGE = getattr(settings, 'YT_MAIN_TEMPLATE_MESSAGE', None) or 'main/message.html'

_CONFIG = {}
_CONFIG['theme'] = 'main'
_CONFIG['site_title'] = u'Site Title'
_CONFIG['site_description'] = u'site description...'

CONFIG = getattr(settings, 'YT_MAIN_CONFIG', _CONFIG)

PLUGINS = getattr(settings, 'YT_MAIN_PLUGINS', ())
