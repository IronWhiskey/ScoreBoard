# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojoPong', '0004_auto_20180427_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firstName',
            new_name='moniker',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastName',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='league',
            name='location',
            field=models.CharField(default='office break room', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='dojoPong.League'),
            preserve_default=False,
        ),
    ]
