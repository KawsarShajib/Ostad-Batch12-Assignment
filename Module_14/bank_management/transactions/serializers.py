from rest_framework import serializers
from decimal import Decimal
from django.db import transaction as db_transaction
from accounts.models import BankAccount
from .models import Transaction


class DepositSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_account_id(self, value):
        user = self.context['request'].user
        try:
            account = BankAccount.objects.get(id=value, owner=user, status='ACTIVE')
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError("Account not found or you do not have permission.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        account = BankAccount.objects.get(id=validated_data['account_id'], owner=user)
        amount = validated_data['amount']
        description = validated_data.get('description', 'Deposit')

        with db_transaction.atomic():
            account.balance += amount
            account.save()
            txn = Transaction.objects.create(
                transaction_type='DEPOSIT',
                amount=amount,
                account=account,
                description=description,
                created_by=user
            )
        return txn


class WithdrawSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user
        try:
            account = BankAccount.objects.get(id=attrs['account_id'], owner=user, status='ACTIVE')
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError({"account_id": "Account not found or you do not have permission."})

        if not account.can_withdraw(attrs['amount']):
            raise serializers.ValidationError({"amount": "Insufficient balance for this withdrawal."})
        attrs['account'] = account
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        account = validated_data['account']
        amount = validated_data['amount']
        description = validated_data.get('description', 'Withdrawal')

        with db_transaction.atomic():
            account.balance -= amount
            account.save()
            txn = Transaction.objects.create(
                transaction_type='WITHDRAWAL',
                amount=amount,
                account=account,
                description=description,
                created_by=user
            )
        return txn


class TransferSerializer(serializers.Serializer):
    from_account_id = serializers.IntegerField()
    to_account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user
        try:
            from_account = BankAccount.objects.get(
                id=attrs['from_account_id'], owner=user, status='ACTIVE'
            )
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError(
                {"from_account_id": "Source account not found or you do not have permission."}
            )

        try:
            to_account = BankAccount.objects.get(
                account_number=attrs['to_account_number'], status='ACTIVE'
            )
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError(
                {"to_account_number": "Destination account not found or is inactive."}
            )

        if from_account.id == to_account.id:
            raise serializers.ValidationError(
                {"to_account_number": "Cannot transfer money to the same account."}
            )

        if not from_account.can_withdraw(attrs['amount']):
            raise serializers.ValidationError(
                {"amount": "Insufficient balance for this transfer."}
            )

        attrs['from_account'] = from_account
        attrs['to_account'] = to_account
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        from_account = validated_data['from_account']
        to_account = validated_data['to_account']
        amount = validated_data['amount']
        description = validated_data.get('description', f'Transfer to {to_account.account_number}')

        with db_transaction.atomic():
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            txn = Transaction.objects.create(
                transaction_type='TRANSFER',
                amount=amount,
                from_account=from_account,
                to_account=to_account,
                description=description,
                created_by=user
            )
        return txn


class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.SerializerMethodField()
    from_account_number = serializers.CharField(source='from_account.account_number', read_only=True, default=None)
    to_account_number = serializers.CharField(source='to_account.account_number', read_only=True, default=None)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, default=None)

    class Meta:
        model = Transaction
        fields = (
            'id', 'transaction_id', 'transaction_type', 'amount',
            'account', 'account_number',
            'from_account', 'from_account_number',
            'to_account', 'to_account_number',
            'description', 'created_at', 'created_by', 'created_by_username'
        )
        read_only_fields = fields

    def get_account_number(self, obj):
        if obj.account:
            return obj.account.account_number
        return None
