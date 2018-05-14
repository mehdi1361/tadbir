from django import template
from django.db.models import Sum
from bank.models import File
register = template.Library()


@register.simple_tag
def add(a, b):
    return a + b


@register.simple_tag
def count_files(user):
    files = File.objects.filter(employees__employee=user)
    return files.count()


@register.simple_tag
def sum_main_deposit(user):
    result = File.objects.filter(employees__employee=user).aggregate(Sum('main_deposit'))
    return result['main_deposit__sum']
