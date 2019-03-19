# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-19 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ding_callback', '0004_auto_20190319_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowinfo',
            name='monitor_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flowinfo', to='ding_callback.MonitorPoint'),
        ),
        migrations.AlterField(
            model_name='sampleinfo',
            name='monitor_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sample', to='ding_callback.MonitorPoint'),
        ),
    ]