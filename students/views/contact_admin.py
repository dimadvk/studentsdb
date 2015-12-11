from django.shortcuts import render

from django import forms

class ContactForm(forms.Form):
    form_email = froms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = froms.CharField(
        label=u"Заголовок Листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2500,
        widget=forms.Textarea)

def contact_admin(request):
    return render(request, 'contact_admin/form.html', {})
