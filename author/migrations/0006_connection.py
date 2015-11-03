# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_auto_20150502_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dhost', models.CharField(max_length=1024)),
                ('dport', models.CharField(max_length=5)),
                ('sport', models.CharField(max_length=5)),
                ('protocol', models.CharField(max_length=3)),
                ('uploaded_image', models.ForeignKey(related_name='connections', to='author.UploadedTaskImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
