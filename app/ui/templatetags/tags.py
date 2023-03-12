from datetime import datetime

from django import template

register = template.Library()

@register.filter
def str_to_date(value):
    return datetime.strptime(value, '%Y-%m-%d')