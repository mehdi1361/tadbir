# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-15 22:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='persondailyreport',
            unique_together=set([('user', 'persian_date')]),
        ),
    ]
