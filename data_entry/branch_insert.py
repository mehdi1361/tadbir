import csv
from bank.models import Branch, ManagementAreas, City


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    city = City.objects.get(name='تهران')
    area = ManagementAreas.objects.get(pk=1)

    for row in reader:
        Branch.objects.create(name=str(row[0]), code=str(row[0]), city=city, area=area)
        print(row[0])


def csv_insert():
    csv_path = "data_entry/branch.csv"

    with open(csv_path, "rt") as f_obj:

        csv_reader(f_obj)