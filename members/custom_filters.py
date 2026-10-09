from django import template

register = template.Library()

@register.filter
def date_ar(value):
    """تنسيق التاريخ بصيغة يوم/شهر/سنة"""
    if value:
        return value.strftime('%d/%m/%Y')
    return ''