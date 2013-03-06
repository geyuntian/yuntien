# Copyright 2009 http://www.yuntien.com
# Licensed under the Apache License, Version 2.0

import datetime
from django import template
from yuntien.base.settings import TIMEZONE_OFFSET

register = template.Library()

@register.filter
def timedelta(dt, delta=TIMEZONE_OFFSET):
    return dt + datetime.timedelta(hours = delta)
