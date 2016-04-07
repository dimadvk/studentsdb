from django import template
from django.core.urlresolvers import resolve

register = template.Library()

@register.simple_tag(takes_context=True)
def select_menu(context, string):
    path = context.get('request').path
    resolved_url_name = resolve(path).url_name
    if resolved_url_name == string:
        return 'class="active"'
    else:
        return ''
