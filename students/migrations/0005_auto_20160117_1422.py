# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.student


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20160114_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, upload_to=b'', null=True, verbose_name='\u0444\u043e\u0442\u043e', ),
            preserve_default=True,
        ),
    ]
