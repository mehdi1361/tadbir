# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-17 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0019_auto_20180414_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='national_code',
            field=models.CharField(max_length=20, null=True, verbose_name='کد ملی'),
        ),
    ]
