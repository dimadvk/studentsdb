from django.contrib import admin
from .models.student import Student
from .models.group import Group

from django.core.urlresolvers import reverse

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']

    def view_on_site(slef, obj):
        return reverse('students_edit', kwargs={'pk':obj.id})


# Register your models here.

admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
