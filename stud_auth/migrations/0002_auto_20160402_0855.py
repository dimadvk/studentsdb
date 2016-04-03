# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stprofile',
            name='address',
            field=models.CharField(default=b'', max_length=256, verbose_name='address', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stprofile',
            name='passport_id',
            field=models.CharField(default=b'', max_length=8, verbose_name='passport id', blank=True),
            preserve_default=True,
        ),
    ]
