import csv
from bank.models import File
from employee.models import EmployeeFile
from django.contrib.auth.models import User


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        try:
            print(row[0], row[12])
            file = File.objects.get(file_code=row[0])
            user = User.objects.get(username=row[12])
            EmployeeFile.objects.create(employee=user, file=file)

        except:
            print('error')


def csv_insert():
    csv_path = "data_entry/file.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)