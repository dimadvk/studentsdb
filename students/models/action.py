from django.db import models
from django.utils.translation import ugettext_lazy as _

class Action(models.Model):
    class Meta:
        verbose_name = _(u'action')
        verbose_name_plural = _(u'actions')

    timestamp = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name=_('action time'),
    )
    user = models.CharField(
        default='UNKNOWN',
        verbose_name=_(u'username'),
        max_length=256,
    )
    action_detail = models.CharField(
        verbose_name=_(u'action descriprion'),
        blank=False,
        max_length=256,
    )
    model_name = models.CharField(
        verbose_name=_(u'model name'),
        blank=False,
        max_length=256,
    )
    model_verbose_name = models.CharField(
        verbose_name=_(u'model verbose name'),
        blank=False,
        max_length=256,
    )

    def __unicode__(self):
        return u"%s (%s)" % (self.model_name, self.model_verbose_name)
