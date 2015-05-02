# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_auto_20150501_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedtask',
            name='author',
            field=models.ForeignKey(related_name='uploaded_task', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
