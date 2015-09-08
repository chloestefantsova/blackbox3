# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_game_send_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='auth_string_length',
            field=models.PositiveIntegerField(default=32, blank=True),
            preserve_default=True,
        ),
    ]
