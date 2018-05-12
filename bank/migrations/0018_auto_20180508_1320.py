# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0017_merge_20180504_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='نام و نام خانوادگی')),
                ('father_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام پدر')),
                ('national_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='کد ملی')),
                ('gender', models.CharField(choices=[('مرد', 'مرد'), ('زن', 'زن')], max_length=20, null=True, verbose_name='جنسیت')),
            ],
            options={
                'verbose_name': 'وکیل',
                'verbose_name_plural': 'وکلا',
                'db_table': 'lawyers',
            },
        ),
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='نام بانک'),
        ),
        migrations.AlterField(
            model_name='filetype',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='نوع پرونده'),
        ),
        migrations.AlterField(
            model_name='historicalbank',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='نام بانک'),
        ),
        migrations.AlterField(
            model_name='historicalfiletype',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='نوع پرونده'),
        ),
        migrations.AlterField(
            model_name='person',
            name='file',
            field=models.ManyToManyField(related_name='persons', through='bank.PersonFile', to='bank.File', verbose_name='پرونده'),
        ),
    ]
