# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, multiplier):
    try:
        return int(value) * int(multiplier)
    except (ValueError, TypeError):
        return value