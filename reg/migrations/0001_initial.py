# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('is_school', models.BooleanField(default=False)),
                ('school_name', models.CharField(max_length=1024, blank=True)),
                ('teacher_name', models.CharField(max_length=256, blank=True)),
                ('teacher_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('leader_email', models.EmailField(max_length=75)),
                ('address', models.TextField(blank=True)),
                ('auth_string', models.CharField(max_length=32, blank=True)),
                ('created_at', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(to='reg.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
