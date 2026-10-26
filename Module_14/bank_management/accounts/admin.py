from django.contrib import admin
from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'owner', 'account_type', 'balance', 'status', 'created_at')
    list_filter = ('account_type', 'status', 'created_at')
    search_fields = ('account_number', 'owner__username', 'owner__email')
    readonly_fields = ('account_number', 'created_at', 'updated_at')
    ordering = ('-created_at',)