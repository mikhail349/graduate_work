from datetime import datetime

from django import template

register = template.Library()


@register.filter
def str_to_date(value):
    return datetime.strptime(value, '%Y-%m-%d')


@register.simple_tag
def get_bg_by_quality(quality: str):
    if quality == 'sd':
        return 'bg-secondary'
    return 'bg-primary'
