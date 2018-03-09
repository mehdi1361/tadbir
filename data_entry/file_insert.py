import csv
from bank.models import File, Branch


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        try:
            state = ''
            branch = Branch.objects.get(code=row[4])
            if row[6] == '**':
                state = 'در حال پیگیری'

            if row[6] == '***':
                state = 'تسویه حساب'

            if row[6] == 'ع':
                state = 'عودت'

            File.objects.get_or_create(
                states=state,
                branch=branch,
                defaults={'file_code': row[0]}
            )

        except:
            print('error')


def csv_insert():
    csv_path = "data_entry/file.csv"

    with open(csv_path, "rt") as f_obj:

        csv_reader(f_obj)