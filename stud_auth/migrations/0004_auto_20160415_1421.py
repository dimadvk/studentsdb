# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0003_auto_20160402_0904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stprofile',
            options={'verbose_name': '\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f \u043f\u0440\u043e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430', 'verbose_name_plural': '\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f \u043f\u0440\u043e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430'},
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='address',
            field=models.CharField(default=b'', max_length=256, verbose_name='\u0430\u0434\u0440\u0435\u0441\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='passport_id',
            field=models.CharField(default=b'', max_length=8, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u043f\u0430\u0441\u043f\u043e\u0440\u0442\u0430', blank=True),
            preserve_default=True,
        ),
    ]
