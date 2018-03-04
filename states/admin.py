from django.contrib import admin
from .models import State, City
# Register your models here.


class CityInline(admin.StackedInline):
    model = City


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')
    inlines = (CityInline, )