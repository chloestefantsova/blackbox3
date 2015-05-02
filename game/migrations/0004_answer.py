# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150502_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(blank=True)),
                ('task', models.ForeignKey(related_name='answers', to='game.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
