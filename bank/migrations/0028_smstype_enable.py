# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 05:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0027_smstype'),
    ]

    operations = [
        migrations.AddField(
            model_name='smstype',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
    ]
