# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students

def journal_list(request):
    students = (
    {'id': 1,
     'first_name': u'Віталій',
     'last_name': u'Подоба'},
    {'id': 2,
     'first_name': u'Андрій',
     'last_name': u'Корост'},
    {'id': 3,
     'first_name': u'Антон',
     'last_name': u'Разгільдяй'}
    )
    return render(request, 'students/journal.html', {'students':students})

