# -*- coding: utf-8 -*-
import csv
from bank.models import ManagementAreas, State, Bank


def csv_reader(file_obj):
    reader = csv.reader(file_obj)

    state = State.objects.get(pk=1)
    bank = Bank.objects.get(pk=1)

    for row in reader:
        ManagementAreas.objects.create(
            id=row[0],
            name=row[1],
            bank=bank,
            state=state,
            status=True
        )

        print(row)


def csv_insert():
    csv_path = "data_entry/area.csv"

    with open(csv_path, "rt", encoding='utf8') as f_obj:

        csv_reader(f_obj)