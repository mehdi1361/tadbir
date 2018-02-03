# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-30 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0016_auto_20180129_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assurance',
            name='person',
        ),
        migrations.AddField(
            model_name='assurance',
            name='file',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='assurances', to='bank.File', verbose_name='پرونده'),
        ),
        migrations.AlterField(
            model_name='assurance',
            name='assurance_type',
            field=models.CharField(choices=[('سفته', 'سفته'), ('چک', 'چک'), ('سند ملکی', 'سند ملکی'), ('سند در رهن', 'سند در رهن')], default='سفته', max_length=50, verbose_name='نوع وثیقه'),
        ),
    ]
