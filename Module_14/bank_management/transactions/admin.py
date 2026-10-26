from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'transaction_type', 'amount',
        'account', 'from_account', 'to_account', 'created_at', 'created_by'
    )
    list_filter = ('transaction_type', 'created_at')
    search_fields = (
        'transaction_id', 'account__account_number',
        'from_account__account_number', 'to_account__account_number',
        'created_by__username'
    )
    readonly_fields = ('transaction_id', 'created_at')
    ordering = ('-created_at',)
