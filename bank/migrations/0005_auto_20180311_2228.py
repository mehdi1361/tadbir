# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-12 05:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_auto_20180309_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='نوع فایل')),
            ],
            options={
                'verbose_name': 'file_types',
                'verbose_name_plural': 'file_types',
                'db_table': 'file_types',
            },
        ),
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank.FileType', verbose_name='نوع پرونده'),
        ),
    ]
