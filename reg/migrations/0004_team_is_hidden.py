# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0003_auto_20150420_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
