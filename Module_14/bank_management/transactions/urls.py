from django.urls import path
from .views import (
    DepositView,
    WithdrawView,
    TransferView,
    TransactionHistoryView,
    AdminTransactionListView,
)

urlpatterns = [
    path('transactions/deposit/', DepositView.as_view(), name='deposit'),
    path('transactions/withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transactions/transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('admin/transactions/', AdminTransactionListView.as_view(), name='admin-transactions'),
]
