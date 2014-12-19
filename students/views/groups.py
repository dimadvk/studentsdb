# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Groups

def groups_list(request):
    groups = (
        {'id':1,
     'name': u'МтМ-21',
         'headman': u'Віталій Подоба'},
        {'id': 2,
     'name': u'МтМ-22',
         'headman': u'Андрій Корост'},
        {'id': 3,
     'name': u'МтМ-23',
         'headman': u'Антон Разгільдяй'}
    )
    return render(request, 'students/groups_list.html', {'groups':groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

