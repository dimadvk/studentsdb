# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

from ..models import Student
from ..models import Journal

# Views for Students

def journal_list(request):
   
    # get month. If no month specified - use current month
    request_month = request.GET.get('month', '')
    if request_month:
        # should be done later
        pass
    else:
        # use the current month:
        current_date = datetime.now()
        month_num = current_date.month
        month_name = current_date.strftime('%B')

    # get name of month
    # get count of days in month
    # get names of every day in month

    # get students
    students = Student.objects.all()

    # get students ids and get journal
    students_ids = students.values_list('id')
    students_journals = Journal.objects.filter(student_id__in=students_ids).all()
    # для конкретного місяця: j = Journal.objects.filter(attendance__month=month)

    return render(request, 'students/journal.html', {'students':students})

