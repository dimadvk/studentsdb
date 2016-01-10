# -*- coding: utf-8 -*-

from django.db import models
from student import Student
from group import Group

# Create your models here

class Journal(models.Model):
    """Journal Model"""
    class Meta(object):
        verbose_name = u"Відвідування"
        verbose_name_plural = "Відвідування"

    student = models. xxx ('Student',
        verbose_name = u'Студент',
        null = False,
        blank = False,
        on_delete = models.SET_NULL)
    
    date = models.DateField(
        blank = False,
        verbose_name = "Був присутній"
        null = False)

    def __unicode__(self):
        return u"%s %s" % (self.student.first_name, self.student.last_name)

