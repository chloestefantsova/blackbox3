# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20150908_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='send_emails',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
