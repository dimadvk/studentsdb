# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='model_name',
            field=models.CharField(default='Student', max_length=256, verbose_name='\u043d\u0430\u0437\u0432\u0430 \u043c\u043e\u0434\u0435\u043b\u0456'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='model_verbose_name',
            field=models.CharField(default='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', max_length=256, verbose_name='\u043f\u043e\u0432\u043d\u0430 \u043d\u0430\u0437\u0432\u0430 \u043c\u043e\u0434\u0435\u043b\u0456'),
            preserve_default=False,
        ),
    ]
