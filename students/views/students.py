# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.forms import  ModelForm, ValidationError
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from ..models.student import Student
from ..models.group import Group
from ..util import paginate, get_current_group

from students_add import StudentAddForm

class StudentUpdateForm(StudentAddForm):
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
    def clean_student_group(self):
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою групи "%s"' % groups.first())
        return self.cleaned_data['student_group']


class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentUpdateForm
    success_message = u'Студента "%(first_name)s %(last_name)s" успішно збережено!'

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context.update({'page_title': u"Редагувати Студента"})
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(self.request, u"Редагування студента відмінено!")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, u"Студента успішно видалено!")
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)

def students_delete_bunch(request):
    if request.method =="POST":
        students_id_list = request.POST.getlist('selected-student')
        students_set = Student.objects.filter(pk__in=students_id_list)
        students_set.delete()
        messages.info(request, u"Вибраних студентів успішно видалено!")
        return HttpResponseRedirect(reverse("home"))


def students_delete(request, pk):
    student = Student.objects.get(pk=pk)
    context = {'object': student}
    if request.method == "GET":
        confirm_template = "students/students_confirm_delete.html"
        return render(request, confirm_template, context)
    elif request.method == "POST":
        student.delete()
        messages.info(request, u"Студента успішно видалено!")
        return HttpResponseRedirect(reverse("home"))

        

# Views for Students

class StudentList(ListView):
    #model = Student
    context_object_name = 'students'
    queryset = Student.objects.values('last_name')


def students_list(request):
    # check if need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
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
    #num_rows_per_page = 4
    #if len(students):
    #    num_pages = len(students) // num_rows_per_page
    #else:
    #    num_pages = 1
    ## if len(students) % num_rows_per_page > 0
    #if len(students) % num_rows_per_page:
    #    num_pages += 1
    #page = request.GET.get('page')
    ## ceck if page is integer
    #try:
    #    page = int(page)
    #except:
    #    page = 1
    ## if page is out of range return last page
    #if page > num_pages:
    #    page = num_pages
    #elif page < 1:
    #    page = 1
    #students = students[ (page-1)*num_rows_per_page : page*num_rows_per_page ]
    #page_list = [p+1 for p in range(num_pages)]

    context = paginate(students, 3, request, {}, var_name='students')

    return render(request, 'students/students_list.html', context)

def students_ajax_next_page(request):
    text = '<h2>Text from view students_ajax_next_page, received via ajax</h2>'
    return HttpResponse(text)
