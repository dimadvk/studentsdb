from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here

class Group(models.Model):
    '''Group Model'''

    class Meta(object):
        verbose_name = _(u"group")
        verbose_name_plural = _(u"groups")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"name"))

    leader = models.OneToOneField('Student',
        verbose_name=_(u"leader"),
        null = True,
        blank = True,
        on_delete = models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"additional notes"))

    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % (self.title, )
