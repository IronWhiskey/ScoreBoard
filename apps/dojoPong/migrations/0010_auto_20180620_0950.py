# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojoPong', '0009_auto_20180619_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='notes',
            field=models.CharField(max_length=255),
        ),
    ]
