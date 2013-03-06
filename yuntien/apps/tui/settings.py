# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.base.views.plugin import *

COMMENT_NUM_PER_PAGE = getattr(settings, 'YT_TUI_COMMENT_NUM_PER_PAGE', None) or 10
RECENT_COMMENT_NUM = getattr(settings, 'YT_TUI_RECENT_COMMENT_NUM', None) or 10

TEMPLATE_404 = getattr(settings, 'YT_TUI_TEMPLATE_404', None) or 'tui/404.html'
TEMPLATE_MESSAGE = getattr(settings, 'YT_TUI_TEMPLATE_MESSAGE', None) or 'tui/message.html'

_CONFIG = {}
_CONFIG['theme'] = 'tui'
_CONFIG['site_title'] = u'Site Title'
_CONFIG['site_description'] = u'site description...'

CONFIG = getattr(settings, 'YT_TUI_CONFIG', _CONFIG)

APP_ID = getattr(settings, 'YT_TUI_APP_ID', 'tui')

PLUGINS = getattr(settings, 'YT_TUI_PLUGINS', ())
