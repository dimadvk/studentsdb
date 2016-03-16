# -*- coding: utf-8 -*-
from django.db import models

class Action(models.Model):
    class Meta:
        verbose_name = u'подія'
        verbose_name_plural = u'події'

    timestamp = models.DateTimeField(
        auto_now_add = True,
        auto_now = False,
        verbose_name = 'час події',
    )
    user = models.CharField(
        default = 'UNKNOWN',
        verbose_name = u'користувач',
        max_length = 256,
    )
    action_detail = models.CharField(
        verbose_name = u'опис події',
        blank = False,
        max_length = 256,
    )
    model_name = models.CharField(
        verbose_name = u'назва моделі',
        blank = False,
        max_length = 256,
    )
    model_verbose_name = models.CharField(
        verbose_name = u'повна назва моделі',
        blank = False,
        max_length = 256,
    )

