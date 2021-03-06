# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-06 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_auto_20180325_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepermission',
            name='permission_type',
            field=models.CharField(choices=[('dashboard', 'داشبورد'), ('employee_file', 'پرونده های کارشناسان'), ('bank_new', 'ایجاد بانک'), ('bank_edit', 'ویرایش بانک'), ('bank_list', 'لیست بانک'), ('area_new', 'سرپرستی جدید'), ('area_edit', 'ویرایش سرپرستی'), ('area_list', 'لیست مناطق'), ('branch_new', 'شعبه جدید'), ('branch_edit', 'ویرایش شعبه'), ('branch_list', 'لیست شعب'), ('sms_list', 'متن پیامک'), ('set_permission', 'تعیین سطح دسترسی'), ('file_new', 'پرونده جدید'), ('file_edit', 'ویرایش پرونده'), ('file_list', 'لیست پرونده ها'), ('office_new', 'شخص حقوقی جدید'), ('office_edit', 'ویرایش شخص حقوقی'), ('office_list', 'لیست اشخاص حقوقی'), ('report_user', 'گزارش عملکرد کارشناسان'), ('report_bank', 'گزارش به تفکیک بانک'), ('role_access', 'تعیین سطح دسترسی'), ('create_employee', 'ایجاد کاربر')], default='dashboard', max_length=100, verbose_name='دسترسی'),
        ),
    ]
