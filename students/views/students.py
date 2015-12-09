# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.student import Student

# Views for Students

def students_list(request):
    students = Student.objects.all()

    # try to order students_list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
        students = students.reverse()
    else:
       order_by = 'last_name'
       students = students.order_by(order_by)

    # # paginate students
    # paginator = Paginator(students, 3)
    # page = request.GET.get('page')
    # try:
    #     students = paginator.page(page)
    # except PageNotAnInteger:
    #     # if page is not an integer, deliver first page.
    #     students = paginator.page(1)
    # except EmptyPage:
    #     # if page is out of range (e.g. 9999), deliver
    #     # last page of results.
    #     students = paginator.page(paginator.num_pages)
    # return render(request, 'students/students_list.html', {'students':students})

    # remake pagination without 'paginator'
    # count of pages:
    num_rows_per_page = 3
    if len(students):
        num_pages = len(students) // num_rows_per_page
    else:
        num_pages = 1
    # if len(students) % num_rows_per_page > 0
    if len(students) % num_rows_per_page:
        num_pages += 1
    page = request.GET.get('page')
    # ceck if page is integer
    try:
        page = int(page)
    except:
        page = 1
    # if page is out of range return last page
    if page > num_pages:
        page = num_pages
    elif page < 1:
        page = 1
    students = students[ (page-1)*num_rows_per_page : page*num_rows_per_page ]
    page_list = [p+1 for p in range(num_pages)]
    return render(request, 'students/students_list.html',
            {'students':students,
            'page':page,
            'num_pages':num_pages,
            'num_rows_per_page':num_rows_per_page,
            'page_list':page_list}
            )

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s' % sid)
