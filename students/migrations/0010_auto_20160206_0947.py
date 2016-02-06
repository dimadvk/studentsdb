# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20160206_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='student',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
    ]
