from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.

    This function takes:
        * list of elements;
        * number of objects per page;
        * request object to get url parameters from;
        * context to set new variables into;
        * var_name - variable name for list of objects.

    It returns updated context object.
    """

    paginator = Paginator(objects, size)

    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context
