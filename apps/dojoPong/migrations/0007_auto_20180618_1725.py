# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojoPong', '0006_auto_20180618_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='rules',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='state',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
