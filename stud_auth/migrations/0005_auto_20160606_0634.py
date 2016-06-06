# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0004_auto_20160415_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stprofile',
            options={'verbose_name': 'Additional User Info', 'verbose_name_plural': 'Additional User Info'},
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='address',
            field=models.CharField(default=b'', max_length=256, verbose_name='address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='mobile_phone',
            field=models.CharField(default=b'', max_length=12, verbose_name='Mobile Phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='passport_id',
            field=models.CharField(default=b'', max_length=8, verbose_name='passport id', blank=True),
            preserve_default=True,
        ),
    ]
