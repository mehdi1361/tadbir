# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0015_mailbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailbox',
            name='star',
            field=models.BooleanField(default=False, verbose_name='نشان گزاری'),
        ),
    ]
