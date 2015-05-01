# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='writeup_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='writeup_ru',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
