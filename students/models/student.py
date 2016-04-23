from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Create your models here

class Student(models.Model):
    '''Student Model'''

    class Meta:
        verbose_name = _(u"student")
        verbose_name_plural = _(u"students")

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"first name"),
    )
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"last name")
    )
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u"middle name"),
        default=''
    )
    birthday = models.DateField(
        blank=False,
        verbose_name=_(u"birthday"),
        null=True
    )
    photo = models.ImageField(
        blank=True,
        verbose_name=_(u"photo"),
        null=True,
    )
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"ticket"),
    )
    student_group = models.ForeignKey(
        'Group',
        verbose_name=_(u"group"),
        blank=False,
        null=True,
        on_delete=models.PROTECT
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Additional notes")
    )
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def clean(self):
        if self.photo:
            if len(self.photo) > (1*1024*1024):
                raise ValidationError({"photo":  _(u'The file is too big. Must be less then 2MB')})


