# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20150501_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(default='unknown', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='cost',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
