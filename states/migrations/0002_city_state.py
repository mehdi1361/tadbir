# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-08 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='states.State', verbose_name='state'),
        ),
    ]
