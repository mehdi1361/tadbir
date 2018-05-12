# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 20:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0018_auto_20180508_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLawyerFile',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical تخصیص وکیل',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='LawyerFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
            options={
                'verbose_name': 'تخصیص وکیل',
                'verbose_name_plural': 'اشخاص حقیقی پرونده',
                'db_table': 'lawyer_files',
            },
        ),
        migrations.AlterField(
            model_name='assurance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='assurance',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='file',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='file',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='fileoffice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='fileoffice',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='filetype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='filetype',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalassurance',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalassurance',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalbank',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalbank',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalbranch',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalbranch',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalfile',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalfile',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalfileoffice',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalfileoffice',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalfiletype',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalfiletype',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalmanagementareas',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalmanagementareas',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicaloffice',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicaloffice',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalpersonfile',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalpersonfile',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='historicalsmstype',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='historicalsmstype',
            name='update_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='managementareas',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='managementareas',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='office',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='office',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='person',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='person',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='personfile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='personfile',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='smstype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='smstype',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AddField(
            model_name='lawyerfile',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lawyers', to='bank.File', verbose_name='پرونده'),
        ),
        migrations.AddField(
            model_name='lawyerfile',
            name='lawyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='bank.Lawyer', verbose_name='وکیل'),
        ),
        migrations.AddField(
            model_name='historicallawyerfile',
            name='file',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bank.File'),
        ),
        migrations.AddField(
            model_name='historicallawyerfile',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicallawyerfile',
            name='lawyer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bank.Lawyer'),
        ),
        migrations.AlterUniqueTogether(
            name='lawyerfile',
            unique_together=set([('file', 'lawyer')]),
        ),
    ]
