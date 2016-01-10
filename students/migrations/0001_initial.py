# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u043d\u0430\u0437\u0432\u0430')),
                ('notes', models.TextField(verbose_name='\u0434\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
            ],
            options={
                'verbose_name': '\u0433\u0440\u0443\u043f\u0430',
                'verbose_name_plural': '\u0433\u0440\u0443\u043f\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='\u0456\u043c\u2019\u044f')),
                ('last_name', models.CharField(max_length=256, verbose_name='\u043f\u0440\u0456\u0437\u0432\u0438\u0449\u0435')),
                ('middle_name', models.CharField(default=b'', max_length=256, verbose_name='\u043f\u043e-\u0431\u0430\u0442\u044c\u043a\u043e\u0432\u0456', blank=True)),
                ('birthday', models.DateField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u0440\u043e\u0434\u0436\u0435\u043d\u043d\u044f')),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='\u0444\u043e\u0442\u043e', blank=True)),
                ('ticket', models.CharField(max_length=256, verbose_name='\u0411\u0456\u043b\u0435\u0442')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0413\u0440\u0443\u043f\u0430', to='students.Group', null=True)),
            ],
            options={
                'verbose_name': '\u0441\u0442\u0443\u0434\u0435\u043d\u0442',
                'verbose_name_plural': '\u0441\u0442\u0443\u0434\u0435\u043d\u0442\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='\u0441\u0442\u0430\u0440\u043e\u0441\u0442\u0430'),
            preserve_default=True,
        ),
    ]
