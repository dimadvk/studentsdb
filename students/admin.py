# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models.student import Student
from .models.group import Group


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """ Check if student is leader in any group
        If yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи',
                code='invalid')

        return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form  = StudentFormAdmin

    def view_on_site(slef, obj):
        return reverse('students_edit', kwargs={'pk':obj.id})


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """ Check if leader is in the same group """
        #queryset = Student.objects.filter(student_group=self.instance)
        new_leader = self.cleaned_data['leader']
        queryset = Student.objects.filter(pk=new_leader.pk, student_group=self.instance.pk)
        if len(queryset) == 0:
            raise ValidationError(u"Студент не входить до даної групи!",
                code='invalid')
        return new_leader

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_per_page = 10
    list_filter = ['title', 'leader']
    search_fields = ['title', 'leader__first_name', 'leader__last_name']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('group_edit', kwargs={'pk': obj.pk})
    
# Register your models here.

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
