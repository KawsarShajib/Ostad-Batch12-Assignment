from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('CLOSED', 'Closed'),
    )

    account_number = models.CharField(max_length=20, unique=True, editable=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        # never negative
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering & admin display names
        ordering = ['-created_at']
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

    def __str__(self):
        # for a nice display in admin
        return f"{self.account_number} - {self.owner.username} ({self.account_type})"


    def save(self, *args, **kwargs):
        # Override save() → auto-generate unique account number
        if not self.account_number:
            self.account_number = self._generate_account_number()
        super().save(*args, **kwargs)

    def _generate_account_number(self):
        # Helper method for a unique 12-digit account number
        while True:
            number = str(uuid.uuid4().int)[:12]
            if not BankAccount.objects.filter(account_number=number).exists():
                return number

    def can_withdraw(self, amount):
        # Business rule : Check if withdrawal of given amount is possible
        return self.balance >= amount and self.status == 'ACTIVE'
