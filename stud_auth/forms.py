from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from registration.forms import RegistrationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions


class CustomRegForm(RegistrationForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomRegForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        #self.helper.form_action = ''
        self.helper.form_metho = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10 form-field-width'
        self.helper.layout.append(
            FormActions(
                Submit('add_button', _(u'Register'), css_class='btn btn-primary'),
                HTML(u"<a class='btn btn-link' href='%s'>%s</a>" % (reverse('home'), _(u'Cancel'))),
            )
        )
