# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-08 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0026_auto_20180520_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='type',
            field=models.CharField(choices=[('اسناد ضمه ای', 'اسناد ضمه ای'), ('قرارداد', 'قرارداد')], default='وثیقه', max_length=20, verbose_name='وثایق'),
        ),
    ]
