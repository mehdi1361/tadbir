import csv
from bank.models import Lawyer


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        Lawyer.objects.create(name=row[1], mobile_number=row[0])
        print('mobile:{}, name:{} inserted'.format(row[0], row[1]))


def csv_insert():
    csv_path = "data_entry/lawyer.csv"

    with open(csv_path, "rt", encoding="utf8") as f_obj:

        csv_reader(f_obj)