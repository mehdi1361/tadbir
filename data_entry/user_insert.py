import csv
from django.contrib.auth.models import User


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    # city = City.objects.get(name='تهران')
    # area = ManagementAreas.objects.get(pk=1)

    for row in reader:
        user = User.objects.create_user(username=row[1], password=123456, is_staff=False, is_superuser=True)
        print(row[1])


def csv_insert():
    csv_path = "data_entry/user.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)