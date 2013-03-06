# -*- coding:utf-8 -*-
from django.conf import settings

MAX_TAG_NUM = getattr(settings, 'YT_BASE_MAX_TAG_NUM', None) or 5

TIMEZONE_OFFSET = 0
offset = getattr(settings, 'YT_BASE_TIMEZONE_OFFSET', None)
if offset is not None:
    TIMEZONE_OFFSET = offset

POINTS_HOT = getattr(settings, 'YT_BASE_POINTS_HOT', None) or 5

CACHE_BYPASS_PATH = getattr(settings, 'YT_BASE_CACHE_BYPASS_PATH', ())
