import csv
from bank.models import File, PersonFile, Person


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    for row in reader:
        try:
            person, created = Person.objects.get_or_create(name=row[1])
            file = File.objects.get(file_code=row[0])
            person_file, created = PersonFile.objects.get_or_create(file=file, person=person)
            print(person_file)

        except:
            print('Error')


def csv_insert():
    csv_path = "data_entry/haghaghi.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)