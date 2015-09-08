# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_game_auth_string_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='country_required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
