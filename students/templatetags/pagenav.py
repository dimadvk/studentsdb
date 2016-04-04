from django import template

register = template.Library()

## Usage: {% pagenav object_list=students is_paginated=is_paginated paginator=paginator %}
@register.inclusion_tag('students/pagination.html')
def pagenav(object_list, is_paginated, paginator):
    """Display page navigation for given list of objects"""
    return {
        'object_list': object_list,
        'is_paginated': is_paginated,
        'paginator': paginator,
    }


## Usage: {% pagenav object_list=students is_paginated=is_paginated paginator=paginator %}
#@register.simple_tag
#def pagenav(*args, **kwargs):
#    t = template.loader.get_template('students/pagination.html')
#    return t.render(template.Context({
#        'object_list': kwargs['object_list'],
#        'is_paginated': kwargs['is_paginated'],
#        'paginator': kwargs['paginator'],
#    }))

## Usage: {% pagenav object_list is_paginated paginator %}
#@register.tag
#def pagenav(parser, token):
#    # parse tag arguments
#    try:
#        # split_contents knows how to split quoted strings
#        tag_name, object_list, is_paginated, paginator = token.split_contents()
#    except ValueError:
#        raise template.TemplateSyntaxError("%r tag requires 3 argumnts" %
#                                           token.contents.split()[0])
#    return PageNavNode(object_list, is_paginated, paginator)
#
#
#class PageNavNode(template.Node):
#    def __init__(self, object_list, is_paginated, paginator):
#        self.object_list = template.Variable(object_list)
#        self.is_paginated = template.Variable(is_paginated)
#        self.paginator = template.Variable(paginator)
#
#    def render(self, context):
#        t = template.loader.get_template('students/pagination.html')
#        return t.render(template.Context({
#            'object_list': self.object_list.resolve(context),
#            'is_paginated': self.is_paginated.resolve(context),
#            'paginator': self.paginator.resolve(context),
#        }))
#
