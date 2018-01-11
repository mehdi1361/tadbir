from django.contrib import admin
from .models import Bank, ManagementAreas, Branch


class ManagementInline(admin.TabularInline):
    model = ManagementAreas


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')
    inlines = (ManagementInline, )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')
