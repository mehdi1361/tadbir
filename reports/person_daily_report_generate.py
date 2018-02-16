import jdatetime
from reports.models import PersonDailyReport
from django.contrib.auth.models import User
from random import randint


def main():
    for i in range(1, 12):
        for j in range(1, 30):
            for user in User.objects.all():
                result = {
                    'count_file': randint(100, 500),
                    'value_file': randint(1000000, 1000000000),
                    'count_file_daily': randint(10, 100),
                    'value_file_daily': randint(1000000, 5000000),
                    'count_file_recovery': randint(1, 10),
                    'persian_date': jdatetime.date(1396, i, j),
                    'user': user
                }

                PersonDailyReport.objects.create(**result)


if __name__ == '__main__':
    main()
