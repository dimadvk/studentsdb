# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile_phone', models.CharField(default=b'', max_length=12, verbose_name='\u041c\u043e\u0431\u0456\u043b\u044c\u043d\u0438\u0439 \u0442\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u0444\u0456\u043b\u044c \u041a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430',
            },
            bases=(models.Model,),
        ),
    ]
