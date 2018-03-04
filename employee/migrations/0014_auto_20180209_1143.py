# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-09 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_auto_20180208_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressfile',
            name='type',
            field=models.CharField(choices=[('ملکی', 'ملکی'), ('استیجاری', 'استیجاری'), ('رهنی', 'رهنی')], default='ملکی', max_length=10, verbose_name='نوع مالکیت'),
        ),
    ]
