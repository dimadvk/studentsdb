# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20160221_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd1\x87\xd0\xb0\xd1\x81 \xd0\xbf\xd0\xbe\xd0\xb4\xd1\x96\xd1\x97')),
                ('user', models.CharField(default=b'UNKNOWN', max_length=256, verbose_name='\u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447')),
                ('action_detail', models.CharField(max_length=256, verbose_name='\u043e\u043f\u0438\u0441 \u043f\u043e\u0434\u0456\u0457')),
            ],
            options={
                'verbose_name': '\u043f\u043e\u0434\u0456\u044f',
                'verbose_name_plural': '\u043f\u043e\u0434\u0456\u0457',
            },
            bases=(models.Model,),
        ),
    ]
