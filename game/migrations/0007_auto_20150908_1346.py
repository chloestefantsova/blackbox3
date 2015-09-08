# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='desc_en',
            field=models.TextField(default='Something about the game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='desc_ru',
            field=models.TextField(default=u'\u0427\u0442\u043e-\u043d\u0438\u0431\u0443\u0434\u044c \u043e \u0441\u043e\u0440\u0435\u0432\u043d\u043e\u0432\u0430\u043d\u0438\u0438'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='is_school',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
