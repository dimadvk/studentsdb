# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='action time')),
                ('user', models.CharField(default=b'UNKNOWN', max_length=256, verbose_name='username')),
                ('action_detail', models.CharField(max_length=256, verbose_name='action descriprion')),
                ('model_name', models.CharField(max_length=256, verbose_name='model name')),
                ('model_verbose_name', models.CharField(max_length=256, verbose_name='model verbose name')),
            ],
            options={
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='name')),
                ('notes', models.TextField(verbose_name='additional notes', blank=True)),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonthJournal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('present_day1', models.BooleanField(default=False)),
                ('present_day2', models.BooleanField(default=False)),
                ('present_day3', models.BooleanField(default=False)),
                ('present_day4', models.BooleanField(default=False)),
                ('present_day5', models.BooleanField(default=False)),
                ('present_day6', models.BooleanField(default=False)),
                ('present_day7', models.BooleanField(default=False)),
                ('present_day8', models.BooleanField(default=False)),
                ('present_day9', models.BooleanField(default=False)),
                ('present_day10', models.BooleanField(default=False)),
                ('present_day11', models.BooleanField(default=False)),
                ('present_day12', models.BooleanField(default=False)),
                ('present_day13', models.BooleanField(default=False)),
                ('present_day14', models.BooleanField(default=False)),
                ('present_day15', models.BooleanField(default=False)),
                ('present_day16', models.BooleanField(default=False)),
                ('present_day17', models.BooleanField(default=False)),
                ('present_day18', models.BooleanField(default=False)),
                ('present_day19', models.BooleanField(default=False)),
                ('present_day20', models.BooleanField(default=False)),
                ('present_day21', models.BooleanField(default=False)),
                ('present_day22', models.BooleanField(default=False)),
                ('present_day23', models.BooleanField(default=False)),
                ('present_day24', models.BooleanField(default=False)),
                ('present_day25', models.BooleanField(default=False)),
                ('present_day26', models.BooleanField(default=False)),
                ('present_day27', models.BooleanField(default=False)),
                ('present_day28', models.BooleanField(default=False)),
                ('present_day29', models.BooleanField(default=False)),
                ('present_day30', models.BooleanField(default=False)),
                ('present_day31', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'month journal',
                'verbose_name_plural': 'month journals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='first name')),
                ('last_name', models.CharField(max_length=256, verbose_name='last name')),
                ('middle_name', models.CharField(default=b'', max_length=256, verbose_name='middle name', blank=True)),
                ('birthday', models.DateField(null=True, verbose_name='birthday')),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='photo', blank=True)),
                ('ticket', models.CharField(max_length=256, verbose_name='ticket')),
                ('notes', models.TextField(verbose_name='Additional notes', blank=True)),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='group', to='students.Group', null=True)),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='student', to='students.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='leader'),
            preserve_default=True,
        ),
    ]
