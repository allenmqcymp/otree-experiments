from django import template
from django.utils.safestring import mark_safe

import json

register = template.Library()

from ..models import Constants

# custom tag for getting the payoff in a groups instance
# - because I don't know how to simultaneously loop through groups, and obtain player instances
@register.simple_tag
def player_payoff_by_role(g, role):
    return g.get_payoff_by_role(role)

@register.simple_tag
def revenue_by_round_number(round_num):
    return Constants.REVENUE[round_num]

@register.simple_tag
def forecast_by_round_number(round_num):
    return Constants.REVENUE_CATEGORY[round_num]

@register.simple_tag
def get_field_group(group, field):
    return getattr(group, field)

# referenced from
# https://stackoverflow.com/questions/298772/django-template-variables-and-javascript/1187881#1187881
# use the | js tag to mark complex python data structures safe for use when passing into js
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

# dynamic array lookup in django
# because django will treat x as a name and not use it's value when you try to do:
# arr.x
@register.filter
def lookup(d, key, offset=True):
    print(d)
    print(key)
    return d[key]

@register.filter
def caps(s):
    return s.upper()



