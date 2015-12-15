from django.views.generic import ListView
from ..models.student import Student

class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template = 'students/student_class_based_view_template'

    def get_context_data(self, **kwargs):
        """ this method adds extra variables to template """
        #get original context data from parent class
        context = super(StudentList, self).get_context_data(**kwargs)

        # tell template not to know logo on a page
        context['show_logo'] = False

        # return context mapping
        return context


    def get_queryset(self):
        """ Order students py last_name."""
        # get original query set
        qs = super(StudentList, self).get_queryset()

        # order by last name
        return qs.order_by('last_name')


