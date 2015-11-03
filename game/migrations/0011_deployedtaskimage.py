# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_auto_20150502_1534'),
        ('game', '0010_game_country_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployedTaskImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suffix', models.CharField(max_length=1024)),
                ('host', models.CharField(max_length=1024)),
                ('port', models.CharField(max_length=5)),
                ('task', models.ForeignKey(related_name='deployed_images', to='game.Task')),
                ('uploaded_image', models.ForeignKey(related_name='deployed_images', to='author.UploadedTaskImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
