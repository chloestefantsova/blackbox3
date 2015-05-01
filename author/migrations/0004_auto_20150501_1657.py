# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_uploadedtask_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtaskfile',
            name='original_name',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uploadedtaskimage',
            name='original_name',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
    ]
