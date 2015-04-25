# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_ru', models.CharField(max_length=256)),
                ('title_en', models.CharField(max_length=256)),
                ('desc_ru', models.TextField()),
                ('desc_en', models.TextField()),
                ('flag', models.CharField(max_length=1024)),
                ('is_case_insensitive_check', models.BooleanField(default=False)),
                ('is_trimmed_check', models.BooleanField(default=False)),
                ('check', models.CharField(max_length=2, choices=[(b'EQ', b'Equals'), (b'RE', b'Regex')])),
                ('created_at', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
