# -*- coding: utf-8 -*-
# writed as at https://atsoftware.de/2015/02/django-contact-form-full-tutorial-custom-example-in-django-1-7/
from collections import OrderedDict
from django import forms
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import FormView

from contact_form.forms import ContactForm


class CustomContactForm(ContactForm):
    def __init__(self, request, *args, **kwargs):
        super(CustomContactForm, self).__init__(request=request, *args, **kwargs)
        fields_keyOrder = ['name', 'email', 'body']
        self.fields = OrderedDict((field_name, self.fields[field_name]) for field_name in fields_keyOrder)
    recepient_list = [settings.ADMIN_EMAIL]
    name = forms.CharField(max_length=100,
                           label=u'Ім’я')
    email = forms.EmailField(max_length=200,
                             label=(u'Email адреса'))
    body = forms.CharField(widget=forms.Textarea,
                           label=(u'Повідомлення'))

class CustomContactFormView(FormView):
    form_class = CustomContactForm
    template_name = 'contact_form/contact_form.html'

    def form_valid(self, form):
        form.save()
        return super(CustomContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CustomContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('contact_form_sent')
