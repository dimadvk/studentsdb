# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.models.student


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_journal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='\u0456\u043c\u2019\u044f'),
            preserve_default=True,
        ),
    ]
