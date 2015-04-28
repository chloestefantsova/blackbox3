# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedTaskDeployStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase', models.CharField(blank=True, max_length=2, choices=[(b'FC', b'format check'), (b'UT', b'untar'), (b'MV', b'move files'), (b'EM', b'email docker deployers'), (b'MT', b'make task')])),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(blank=True)),
                ('uploaded_task', models.ForeignKey(related_name='status', to='author.UploadedTask')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadedTaskFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('untarred_path', models.CharField(max_length=1024, blank=True)),
                ('relative_path', models.CharField(max_length=1024, blank=True)),
                ('uploaded_task', models.ForeignKey(related_name='files', to='author.UploadedTask')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadedTaskImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tcp_ports_str', models.CharField(max_length=1024, blank=True)),
                ('udp_ports_str', models.CharField(max_length=1024, blank=True)),
                ('untarred_path', models.CharField(max_length=1024, blank=True)),
                ('relative_path', models.CharField(max_length=1024)),
                ('uploaded_task', models.ForeignKey(related_name='images', to='author.UploadedTask')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='uploadedtask',
            name='format_checks_passed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uploadedtask',
            name='untarred_path',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskuploadprogress',
            name='uploaded_task',
            field=models.ForeignKey(related_name='progress', to='author.UploadedTask'),
            preserve_default=True,
        ),
    ]
