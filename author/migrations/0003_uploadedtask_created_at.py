# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_auto_20150428_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtask',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
