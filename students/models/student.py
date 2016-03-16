# -*- coding: utf-8 -*-

from django.db import models

from django.utils.image import Image
from django.core.exceptions import ValidationError


# Create your models here

class Student(models.Model):
    '''Student Model'''

    class Meta:
        verbose_name = u"студент"
        verbose_name_plural = u"студенти"

    first_name = models.CharField(
        max_length=256,
        blank= False,
        verbose_name=u"ім’я",
    )
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"прізвище"
    )
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"по-батькові",
        default=''
    )
    birthday = models.DateField(
        blank=False,
        verbose_name=u"дата родження",
        null=True
    )
    photo = models.ImageField(
        blank=True,
        verbose_name=u"фото",
        null=True,
    )
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет"
    )
    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT
    )
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки"
    )
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def clean(self):
        if self.photo:
            if len(self.photo) > (1*1024*1024):
                raise ValidationError({"photo": "The file is too big. Must be less than 2MB."})


