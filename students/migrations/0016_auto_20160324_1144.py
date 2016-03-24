# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_auto_20160316_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'verbose_name': 'action', 'verbose_name_plural': 'actions'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'group', 'verbose_name_plural': 'groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'month journal', 'verbose_name_plural': 'month journals'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'student', 'verbose_name_plural': 'students'},
        ),
        migrations.AlterField(
            model_name='action',
            name='action_detail',
            field=models.CharField(max_length=256, verbose_name='action descriprion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='model_name',
            field=models.CharField(max_length=256, verbose_name='model name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='model_verbose_name',
            field=models.CharField(max_length=256, verbose_name='model verbose name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='action time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.CharField(default=b'UNKNOWN', max_length=256, verbose_name='username'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='leader'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(verbose_name='additional notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='student', to='students.Student'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='birthday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='first name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='last name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='middle name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(verbose_name='Additional notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='group', to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(max_length=256, verbose_name='ticket'),
            preserve_default=True,
        ),
    ]
