# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojoPong', '0010_auto_20180620_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='location',
            field=models.CharField(default='downtown office break room', max_length=255),
        ),
        migrations.AlterField(
            model_name='record',
            name='notes',
            field=models.TextField(default='Enter league rules here...'),
        ),
    ]
