# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendance', models.DateField(verbose_name='\u0411\u0443\u0432 \u043f\u0440\u0438\u0441\u0443\u0442\u043d\u0456\u0439')),
                ('student', models.ForeignKey(verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student', unique_for_date=b'attendance_date')),
            ],
            options={
                'verbose_name': '\u0432\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u0432\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
            },
            bases=(models.Model,),
        ),
    ]
