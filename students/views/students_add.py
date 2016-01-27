# -*- coding: utf-8 -*-

from datetime import datetime
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms import ModelForm

from django.utils.image import Image

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from ..models.group import Group
from ..models.student import Student

class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add button
        self.helper.layout.append(
            FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            )
        )
        



def students_add(request):
    form = StudentAddForm()
    context = {'form': form}
    context.update({'page_title': u"Додати Студента"})
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # error collection
            errors = OrderedDict()
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
                try:
                    Image.open(photo).verify()
                except Exception:
                    errors['photo'] = u"Файл не є зображенням"
                else:
                    if photo.size > (2*1024*1024):
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
                for error_key in errors.keys():
                    messages.error(request, errors[error_key])
                context['errors'] = errors

                return render(request, 'students/students_add.html',
                    context)
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
            context)
