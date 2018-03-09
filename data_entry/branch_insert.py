import csv
from bank.models import Branch, ManagementAreas, City


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    city = City.objects.get(pk=1)

    for row in reader:
        # Branch.objects.create(name=str(row[0]), code=str(row[0]), city=city, area=area)
        area = ManagementAreas.objects.get(pk=row[0])
        Branch.objects.create(name=row[2], code=row[1], area=area, city=city)
        print(row, area)


def csv_insert():
    csv_path = "data_entry/branch.csv"

    with open(csv_path, "rt") as f_obj:

        csv_reader(f_obj)