from django import template
register = template.Library()

@register.filter(name='get_dict')
def get_dict(v):
    return v.__dict__

@register.filter(name='get_val')
def get_val(value, arg):
    return value[str(arg)]