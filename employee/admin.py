from django.contrib import admin
from .models import EmployeeFile, DocumentFile
# Register your models here.


@admin.register(EmployeeFile)
class EmployeeFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'employee', 'status')
    search_fields = ('employee', )
    list_filter = ['status']


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'type')
    search_fields = ('file', )
