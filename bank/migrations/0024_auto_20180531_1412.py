# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0023_auto_20180511_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='persian_date_refrence',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='تاریخ ارجاع'),
        ),
        migrations.AlterField(
            model_name='historicalfile',
            name='persian_date_refrence',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='تاریخ ارجاع'),
        ),
    ]
