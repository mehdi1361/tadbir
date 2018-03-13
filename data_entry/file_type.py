import csv
from bank.models import FileType


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    lst_data = []
    for row in reader:
        row_data = row[0].strip()
        if row_data not in lst_data:
            lst_data.append(row_data)

    print(lst_data)

    for row in lst_data:
        FileType.objects.create(name=row)
        print('data {} inserted'.format(row))


def csv_insert():
    csv_path = "data_entry/file_type.csv"

    with open(csv_path, "rt", encoding="utf8") as f_obj:

        csv_reader(f_obj)