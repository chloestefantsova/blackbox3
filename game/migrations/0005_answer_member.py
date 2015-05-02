# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0005_auto_20150420_2353'),
        ('game', '0004_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='member',
            field=models.ForeignKey(related_name='answers', default=None, to='reg.Member'),
            preserve_default=False,
        ),
    ]
