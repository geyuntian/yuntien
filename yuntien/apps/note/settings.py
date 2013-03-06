# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.base.views.plugin import *

NUM_PER_PAGE = getattr(settings, 'YT_NOTE_NUM_PER_PAGE', None) or 10
COMMENT_NUM_PER_PAGE = getattr(settings, 'YT_NOTE_COMMENT_NUM_PER_PAGE', None) or 10
RECENT_COMMENT_NUM = getattr(settings, 'YT_NOTE_RECENT_COMMENT_NUM', None) or 10
TAG_LIMIT = getattr(settings, 'YT_NOTE_TAG_LIMIT', None) or 40

_CONFIG = {}
_CONFIG['theme'] = 'community'
_CONFIG['words'] = 30
_CONFIG['site_title'] = u'Site Title'
_CONFIG['site_description'] = u'site description...'

CONFIG = getattr(settings, 'YT_NOTE_CONFIG', _CONFIG)

APP_ID = getattr(settings, 'YT_NOTE_APP_ID', 'note')

PLUGINS = getattr(settings, 'YT_NOTE_PLUGINS', ())
