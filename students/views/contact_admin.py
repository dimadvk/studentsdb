import logging

from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from studentsdb.settings import ADMIN_EMAIL

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..signals import contact_admin_sent


class ContactAdminForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # call original initialiazator
        super(ContactAdminForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10 form-field-width'

        # form buttons
        self.helper.add_input(Submit('send_button', _(u'Send')))

    from_email = forms.EmailField(
        label=_(u"Your email"))

    subject = forms.CharField(
        label=_(u"Message title"),
        max_length=128)

    message = forms.CharField(
        label=_(u"Message"),
        max_length=2500,
        widget=forms.Textarea)

    recipient_list = [ADMIN_EMAIL]

    def send_email(self):
        data = self.cleaned_data
        send_mail('[contact admin]' + data.get('subject'),
                  'From: ' + data.get('from_email') + '\n\n' + data.get('message'),
                  data.get('from_email'),
                  [ADMIN_EMAIL]
                 )



class ContactAdminView(FormView):
    form_class = ContactAdminForm
    template_name = 'contact_admin/form.html'

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, *args, **kwargs):
        return super(ContactAdminView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contact_admin')

    def form_valid(self, form):
        try:
            form.send_email()
        except Exception:
            message = _(u"Some trouble happend. Message not sent. Please, try later.")
            messages.info(self.request, message)
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            messages.info(self.request, _(u"Message sent successfully"))
            # send a signal
            form_data = self.get_form_kwargs().get('data')
            message_subject = form_data.get('subject')
            message_sender = form_data.get('from_email')
            contact_admin_sent.send(sender=self.__class__,
                                    message_subject=message_subject,
                                    message_sender=message_sender
                                   )
        return super(ContactAdminView, self).form_valid(form)



'''
def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it
        # with data from the request
        form = ContactAdminForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            try:
                send_mail(subject, from_email+'\n\n'+message, from_email, [ADMIN_EMAIL])
            except Exception:
                messages.info(
                    request,
                    u"""Error""")
            else:
                messages.info(request, u"Message sent")

            # redirect to same contact page with messages
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        context = { 'form': ContactAdminForm()}

    return render(request, 'contact_admin/form.html', context)
'''
