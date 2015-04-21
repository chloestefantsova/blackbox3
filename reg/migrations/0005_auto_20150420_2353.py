# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0004_team_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
            preserve_default=True,
        ),
    ]
