from django import template

register = template.Library()

@register.assignment_tag()
def assign_variable(*args):
    """
    in template:
        {% assign_variable var1 var2 as var %}
    background logic:
        if var1 exists:
            var = var1
        else:
            var = var2
        return var
    """
    if args[0]:
        variable = args[0]
    else:
        variable = args[1]
    return variable
