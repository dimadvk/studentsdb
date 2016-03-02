# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

from django.shortcuts import render, redirect
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import FormView

from studentsdb.settings import ADMIN_EMAIL, DEFAULT_FROM_EMAIL

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
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок Листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2500,
        widget=forms.Textarea)

    recipient_list = [ADMIN_EMAIL]

    def send_email(self):
        data = self.cleaned_data
        send_mail('[contact admin]' + data.get('subject'),
                  'From: ' + data.get('from_email') + '\n\n' + data.get('message'),
                  DEFAULT_FROM_EMAIL,
                  [ADMIN_EMAIL]
                 )



class ContactAdminView(FormView):
    form_class = ContactAdminForm
    template_name = 'contact_admin/form.html'

    def get_success_url(self):
        return reverse('contact_admin')

    def form_valid(self, form):
        try:
            form.send_email()
        except Exception:
            message = u"Сталася якась помилка, лист не відправився. Shit happens :)"
            messages.info(self.request, message)
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            messages.info(self.request, u"Лист відправлено. Верховна канцелярія вже займається обробкою!")
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
                    u"""Під час віправки листа виникла непередабачувана помилка.
                    Спробуйте скористатися данною формою пізніше.""")
            else:
                messages.info(request, u"Повідомлення успішно надіслане")

            # redirect to same contact page with messages
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        context = { 'form': ContactAdminForm()}

    return render(request, 'contact_admin/form.html', context)
'''
