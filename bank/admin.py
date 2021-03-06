from django.contrib import admin
from .models import Bank, ManagementAreas, Branch, File, SmsType, FileType


class ManagementInline(admin.TabularInline):
    model = ManagementAreas


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')
    inlines = (ManagementInline, )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')


@admin.register(FileType)
class FileTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'file_code',
        'contract_code',
        'main_deposit',
        'nc_deposit',
        'so_deposit',
        'cost_proceeding',
        'branch',
        'status',
        'created_at',
        'update_at'
    )


@admin.register(SmsType)
class SmsTypeAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'detail'
    )
