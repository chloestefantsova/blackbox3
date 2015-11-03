# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20151103_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='starts_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
