# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-27 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ding_callback', '0007_monitorpoint_people'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorpoint',
            name='people',
            field=models.CharField(default='梁昊', max_length=32, verbose_name='监测者'),
            preserve_default=False,
        ),
    ]
