from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    AccountListCreateView, AccountDetailView, AccountBalanceView,
    AdminCustomerListView, AdminAccountListView,
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # Accounts (customer)
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:id>/', AccountDetailView.as_view(), name='account-detail'),
    path('accounts/<int:id>/balance/', AccountBalanceView.as_view(), name='account-balance'),

    # Admin
    path('admin/customers/', AdminCustomerListView.as_view(), name='admin-customers'),
    path('admin/accounts/', AdminAccountListView.as_view(), name='admin-accounts'),   
]