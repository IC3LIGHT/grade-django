import re

from django import template

register = template.Library()


@register.filter(name='split_at')
def split_at(value, delimiter='@'):
    return value.split(delimiter)[0]


@register.filter
def link_match(value, arg):
    try:
        return re.match(arg, value) is not None
    except re.error:
        return False
