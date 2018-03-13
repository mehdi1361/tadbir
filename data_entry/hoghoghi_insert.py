import csv
from bank.models import Office, File, FileOffice, City


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        try:
            city = City.objects.get(pk=1)
            office, created = Office.objects.get_or_create(name=row[1], city=city)
            file = File.objects.get(file_code=row[0])
            file_office, created = FileOffice.objects.get_or_create(file=file, office=office)
            print(file_office)

        except:
            print('Error')


def csv_insert():
    csv_path = "data_entry/hoghooghi.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)