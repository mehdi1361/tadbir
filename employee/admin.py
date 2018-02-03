from django.contrib import admin
from .models import EmployeeFile
# Register your models here.


@admin.register(EmployeeFile)
class EmployeeFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'employee', 'status')
    search_fields = ('employee', )
    list_filter = ['status']