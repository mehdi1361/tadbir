from datetime import datetime
from django_cron import CronJobBase, Schedule
from common.utils import SmsSender
from employee.models import SmsCaution
from django.core import management

class SmsSenderJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'employee.sms_sender_cron'    # a unique code

    def do(self):
        for sms_list in SmsCaution.objects.filter(status='در صف ارسال'):
            message = '{}\n{}'.format(
                sms_list.mobile_number.phone_owner.person.full_name,
                sms_list.type.detail
            )
            sender = SmsSender(to=sms_list.mobile_number, text=message)
            result = sender.send()
            if result['SendSmsResult'] == 1:
                sms_list.status = 'ارسال شد'

            else:
                sms_list.status = 'خطا در زمان ارسال'

            sms_list.save()


class Backup(CronJobBase):
    RUN_AT_TIMES = ['23:50']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'employee.Backup'

    def do(self):
        file_name = '{}{}{}.gz'.format(
            datetime.now().year,
            datetime.now().month
            if datetime.now().month > 10 else '0{}'.format(datetime.now().month),
            datetime.now().day
        )
        management.call_command('dbbackup', '-z', '-o {}'.format(file_name))