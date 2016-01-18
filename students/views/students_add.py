# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from django.utils.image import Image

from ..models.group import Group
from ..models.student import Student

from datetime import datetime


def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # error collection
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім’я є обов’язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                data['birthday'] = birthday
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть корректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть групу для студента"
                else:
                    data['student_group'] = Group.objects.get(pk=student_group)

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo
                try:
                    Image.open(photo).verify()
                except Exception:
                    errors['photo'] = u"Файл не є зображенням"
                else:
                    if len(photo) > (2*1024*1024):
                        errors['photo'] = u"Завеликий файл. Фото має бути не більше 2 мегабайт"
                    else:
                        data['photo'] = photo

            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()

                # redirect user to students list
                messages.info(
                    request,
                    u'Студента "%s %s" успішно додано!' %
                        (student.first_name, student.last_name),
                )
                return HttpResponseRedirect(reverse('home'))

            else:
                # render form with errors  and previous user input
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                     'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.info(
                request,
                u'Додавання студента скасовано!',
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
            {'groups': Group.objects.all().order_by('title')})
