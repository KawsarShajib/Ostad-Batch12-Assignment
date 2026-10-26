from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from accounts.models import BankAccount
from .models import Transaction
from .serializers import (
    DepositSerializer,
    WithdrawSerializer,
    TransferSerializer,
    TransactionSerializer,
)


class DepositView(APIView):
    """Deposit money into an account."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            txn = serializer.save()
            return Response({
                'message': 'Deposit successful.',
                'transaction': TransactionSerializer(txn).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):
    """Withdraw money from an account."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            txn = serializer.save()
            return Response({
                'message': 'Withdrawal successful.',
                'transaction': TransactionSerializer(txn).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(APIView):
    """Transfer money between accounts."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            txn = serializer.save()
            return Response({
                'message': 'Transfer successful.',
                'transaction': TransactionSerializer(txn).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryView(generics.ListAPIView):
    """View transaction history of own accounts (paginated, filterable by type)."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            qs = Transaction.objects.all()
        else:
            # Transactions related to any of the user's accounts
            user_accounts = BankAccount.objects.filter(owner=user)
            qs = Transaction.objects.filter(
                Q(account__in=user_accounts) |
                Q(from_account__in=user_accounts) |
                Q(to_account__in=user_accounts)
            ).distinct()

        # Filter by transaction type if provided
        txn_type = self.request.query_params.get('type', None)
        if txn_type:
            qs = qs.filter(transaction_type=txn_type.upper())

        return qs


class AdminTransactionListView(generics.ListAPIView):
    """Admin: view all transaction records."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]
