# Copyright 2009 http://www.yuntien.com
# Licensed under the Apache License, Version 2.0

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def encode(str, encoding='utf-8'):
  return str.encode(encoding)
