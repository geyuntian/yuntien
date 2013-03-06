# -*- coding:utf-8 -*-
from django.conf import settings
from yuntien.app.apps import DEFAULT_APPS

APPS = getattr(settings, 'YT_COMMUNITY_APPS', DEFAULT_APPS)

APP_API_STATUS_URL = '/_admin/status/url'
APP_API_STATUS_RENDER = '/_admin/status/render'
