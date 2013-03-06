# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.base.views.plugin import *

POST_NUM_PER_PAGE = getattr(settings, 'YT_FORUM_POST_NUM_PER_PAGE', None) or 20
COMMENT_NUM_PER_PAGE = getattr(settings, 'YT_FORUM_COMMENT_NUM_PER_PAGE', None) or 10
RECENT_POST_NUM = getattr(settings, 'YT_FORUM_RECENT_POST_NUM', None) or 10

_CONFIG = {}
_CONFIG['site_title'] = u'Site Title'
_CONFIG['site_description'] = u'site description...'

CONFIG = getattr(settings, 'YT_FORUM_CONFIG', _CONFIG)

APP_ID = getattr(settings, 'YT_FORUM_APP_ID', 'forum')

PLUGINS = getattr(settings, 'YT_FORUM_PLUGINS', ())
