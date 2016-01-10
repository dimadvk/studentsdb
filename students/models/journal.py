# -*- coding: utf-8 -*-

from django.db import models

# Create your models here

class Journal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name = u'відвідування'
        verbose_name_plural = 'відвідування'

    attendance = models.DateField(
        verbose_name = u'Був присутній',
    )

    student = models.ForeignKey('Student',
        verbose_name = u'Студент',
        on_delete = models.CASCADE,
        unique_for_date = 'attendance_date',
    )

    def __unicode__(self):
        return u"%s %s" % (self.student.first_name, self.student.last_name)

