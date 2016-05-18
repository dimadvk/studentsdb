from datetime import datetime
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms import ModelForm
from django.utils.image import Image
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions

from ..models.group import Group
from ..models.student import Student

#class StudentAddForm(forms.Form):
#    queryset = Group.objects.all()
#
#    student_group = forms.ModelChoiceField(queryset=queryset)
#    def __init__(self, *args, **kwargs):
#            super(StudentAddForm, self).__init__(*args, **kwargs)
#            self.fields['student_group'].queryset = Group.objects.all()

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
        self.helper.form_class = 'form-horizontal student-form'

        # set form field properties
        self.helper.help_text_inline = True
        #self.helper.html5_required = False
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10 form-field-width'

        # add button
        self.helper.layout.append(
            FormActions(
                Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
                HTML(u"<a class='btn btn-link' href='%s'>%s</a>" % (reverse('home'), _(u'Cancel'))),
            )
        )
        #self.helper.layout[3] = AppendedText('birthday',
        #    '<i class="glyphicon glyphicon-calendar" ></i>',
        #    active=True)



@login_required
def students_add(request):
    form = StudentAddForm(request.POST or None)
    context = {'form': form}
    context.update({'page_title': _(u"Add Student")})
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
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Birthday date is required")
            else:
                data['birthday'] = birthday
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(u"Please, enter the correct date (Ex. 1984-12-30)")
                else:
                    data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Select group for student")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Select group for student")
                else:
                    data['student_group'] = Group.objects.get(pk=student_group)

            photo = request.FILES.get('photo')
            if photo:
                if photo.size > (2*1024*1024):
                    errors['photo'] = _(u'The file is too big. Must be less then 2MB')
                else:
                    try:
                        Image.open(photo).verify()
                    except Exception:
                        errors['photo'] = _(u"File is not an image")
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
                    _(u'Student "%(first_name)s %(last_name)s" sucessfully added!') %
                    {'first_name': student.first_name, 'last_name': student.last_name},
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
                _(u'Adding a student got canceled!'),
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
            context)
