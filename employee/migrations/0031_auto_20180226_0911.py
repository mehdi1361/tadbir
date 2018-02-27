# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-26 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0030_auto_20180226_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefile',
            name='status',
            field=models.CharField(choices=[('فعال', 'enable'), ('غیرفعال', 'disable')], default='enable', max_length=50, verbose_name='وضعیت'),
        ),
    ]
