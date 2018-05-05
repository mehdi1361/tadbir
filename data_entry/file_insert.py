import csv
from bank.models import File, Branch, FileType


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        # file_type = None
        # branch = None
        # state = 'در حال پیگیری'
        try:
            print(row[0])
            branch = Branch.objects.get(code=row[13])
            if row[14] == '**':
                state = 'در حال پیگیری'

            elif row[14] == '***':
                state = 'تسویه حساب'

            elif row[14] == 'ع':
                state = 'عودت'

            else:
                state = 'در حال پیگیری'


            try:

                file_type = FileType.objects.get(pk=row[6])

            except:
                file_type = FileType.objects.get(pk=1)

            File.objects.create(
                file_code=row[0],
                contract_code=row[2],
                main_deposit=row[3] if row[3] != '' else 0,
                nc_deposit=row[4] if row[4] != '' else 0,
                so_deposit=row[5] if row[5] != '' else 0,
                file_type=file_type,
                branch=branch,
                states=state
            )

        except:
            print('error')


def csv_insert():
    csv_path = "data_entry/file.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)