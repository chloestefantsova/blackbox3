# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_deployedtaskimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployedtaskimage',
            name='task',
        ),
        migrations.RemoveField(
            model_name='deployedtaskimage',
            name='uploaded_image',
        ),
        migrations.DeleteModel(
            name='DeployedTaskImage',
        ),
    ]
