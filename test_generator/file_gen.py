import random
from bank.models import File, Branch


def main():
    for branch in Branch.objects.all():
        for i in range(10):
            data = {
                'file_code': random.randint(1000000, 9000000),
                'contract_code': random.randint(1000000, 9000000),
                'main_deposit': random.randint(1000000, 900000000),
                'cost_proceeding': random.randint(1000000, 900000000),
                'branch': branch,
                'persian_date_refrence': '{}/{}/{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                ),
                'persian_normal_date_refrence': '{}{}{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                )
            }
            File.objects.create(**data)
            print('mashkook:{}'.format(i))

            data = {
                'file_code': random.randint(1000000, 9000000),
                'contract_code': random.randint(1000000, 9000000),
                'main_deposit': random.randint(1000000, 900000000),
                'cost_proceeding': random.randint(1000000, 900000000),
                'branch': branch,
                'status': 'معوق',
                'persian_date_refrence': '{}/{}/{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                ),
                'persian_normal_date_refrence': '{}{}{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                )
            }
            File.objects.create(**data)
            print('moavagh:{}'.format(i))

            data = {
                'file_code': random.randint(1000000, 9000000),
                'contract_code': random.randint(1000000, 9000000),
                'main_deposit': random.randint(1000000, 900000000),
                'cost_proceeding': random.randint(1000000, 900000000), 'branch': branch,
                'status': 'سر رسید گذشته',
                'persian_date_refrence': '{}/{}/{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                ),
                'persian_normal_date_refrence': '{}{}{}'.format(
                    random.randint(1370, 1395),
                    random.randint(1, 9),
                    random.randint(1, 9)
                )
            }
            File.objects.create(**data)
            print('sar resid:{}'.format(i))


if __name__ == '__main__':
    main()
