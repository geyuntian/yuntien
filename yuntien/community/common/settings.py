# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.app.settings import APPS
from yuntien.framework.settings import *

RESOURCE_URL = getattr(settings, 'YT_RESOURCE_URL', '/static')
DEFAULT_COMMUNITY_LOGO = getattr(settings, 'YT_DEFAULT_COMMUNITY_LOGO', '')

COMMUNITY_REGEX = CONTAINER_ID_REGEX
RESERVED_COMMUNITY_IDS = (u'all', u'add')
RESERVED_WIDGET_IDS = (u'admin', u'members', u'area')
