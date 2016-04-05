from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView, UpdateView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden
from django.forms import ModelForm, ValidationError, ChoiceField, Select
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from crispy_forms.bootstrap import FormActions

from ..models.group import Group
from ..models.student import Student
from ..util import paginate, get_current_group, DispatchLoginRequired 

# Views for Groups

def groups_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(id=current_group.id)
    else:
        groups = Group.objects.all()

    # try to order group list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()
    else:
        order_by = 'title'
        groups = groups.order_by(order_by)

#    # paginate groups
#    paginator = Paginator(groups, 3)
#    page = request.GET.get('page')
#    try:
#        groups = paginator.page(page)
#    except PageNotAnInteger:
#        # if page is not an integer, deliver first page.
#        groups = paginator.page(1)
#    except EmptyPage:
#        # if page is out of range (e.g. 9999), deliver
#        # last page of results.
#        groups = paginator.page(paginator.num_pages)
#    
#    return render(request, 'students/groups_list.html', {'groups':groups})

    # paginate groups with custom func "paginate" from ..util
    context = paginate(groups, 5, request, {}, var_name="groups")
    response = render(request, 'students/groups_list.html', context)
    return response

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10 form-field-width'

        self.helper.layout.append(
            FormActions(
                Submit('edit_button', _(u'Save'), css_class="btn btn-primary"),
                HTML(u"<a class='btn btn-link' href='%s'>%s</a>" % (reverse('groups'), _(u'Cancel'))),
            )
        )
        self.fields['leader'].widget.attrs = {'disabled': 'True'}
        self.fields['leader'].queryset = self.fields['leader'].queryset.none()


class GroupCreateView(DispatchLoginRequired, SuccessMessageMixin, CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = "students/groups_add.html"
    success_url = reverse_lazy("groups")
    success_message = _(u"The group successfully created!")

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context.update({"page_title": _(u"Create Group")})
        return context


#def groups_edit(request, pk):
#    return HttpResponse('<h1>Edit Group %s' % pk)

class GroupUpdateForm(GroupCreateForm):
    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper.form_action = reverse('group_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.fields['leader'].widget.attrs = {}
        self.fields['leader'].queryset = self.instance.student_set.order_by('last_name')

    def clean_leader(self):
        """ Check if leader is in the same group """
        new_leader = self.cleaned_data['leader']
        if hasattr(new_leader, 'student_group') and new_leader.student_group != self.instance:
            raise ValidationError(_(u"The student is not a member of the group!"),
                code='invalid')
        return new_leader
 


class GroupUpdateView(DispatchLoginRequired, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = "students/groups_add.html"
    success_url = reverse_lazy('groups')
    success_message = _(u'The group "%(title)s" successfully saved!')

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context.update({'page_title': _(u'Edit Group')})
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, _(u"Edit canceled"))
            return HttpResponseRedirect(self.success_url)
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

#def groups_delete(request, gid):
#    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
class GroupDeleteView(DispatchLoginRequired, DeleteView):
    model = Group
    template_name = "students/groups_confirm_delete.html"
    success_url = reverse_lazy("groups")

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.student_set.exists():
            messages.info(self.request,
                _(u"Group that contains students couldn't be deleted!"))
            return HttpResponseRedirect(success_url)
        return super(GroupDeleteView, self).delete(request, *args, **kwargs)
