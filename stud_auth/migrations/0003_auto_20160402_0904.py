# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0002_auto_20160402_0855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stprofile',
            options={'verbose_name': 'Additional User Info', 'verbose_name_plural': 'Additional User Info'},
        ),
        migrations.AddField(
            model_name='stprofile',
            name='photo',
            field=models.ImageField(upload_to=b'', verbose_name='photo', blank=True),
            preserve_default=True,
        ),
    ]
