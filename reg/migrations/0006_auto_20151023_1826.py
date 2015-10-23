# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0005_auto_20150420_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='leader_email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
