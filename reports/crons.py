from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User
from django.db.models import Sum
from reports.models import PersonDailyReport
import datetime
import jdatetime


class PersonDailyReportJob(CronJobBase):

    RUN_AT_TIMES = ['23:15']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'reports.person_daily_report_cron_job'

    def do(self):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        for user in User.objects.all():
            count_file = user.files.count()
            value_file = user.files.aggregate(sum=Sum('file__main_deposit'))
            count_file_daily = user.files.filter(created_at__range=
                                                 (today_min, today_max)).count()

            value_file_daily = user.files.filter(created_at__range=(today_min, today_max))\
                .aggregate(sum=Sum('file__main_deposit'))

            daily_report, created = PersonDailyReport.objects.get_or_create(user=user,
                                                                   defaults={'persian_date': jdatetime.date.today()})

            daily_report.count_file = count_file
            daily_report.value_file = value_file['sum']
            daily_report.count_file_daily = count_file_daily
            daily_report.value_file_daily = value_file_daily['sum']
            daily_report.save()







