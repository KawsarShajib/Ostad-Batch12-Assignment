
# **Mini Bank Management System API**

A RESTful API built with **Django** and **Django REST Framework (DRF)** that provides core banking operations for customers: registration, authentication, account management, deposits, withdrawals, money transfers, and transaction history. Admin users can view all customers, accounts, and transactions.

---

## **Project Description**

This project demonstrates:

- REST API design with Django REST Framework
- Token-based authentication
- Proper model relationships (User → BankAccount → Transaction)
- Serializers with validation
- Custom permissions (owner-only + admin)
- Atomic database transactions for money movement
- DecimalField for monetary values
- Pagination and filtering of transaction history
- Clean project structure

**No frontend is included.** 
All endpoints are designed to be tested with Postman, curl, or any HTTP client.

---

## **Technology Used**

| Component              | Version                   |
|------------------------|---------------------------|
| Python                 | 3.10+                     |
| Django                 | 5.0+                      |
| Django REST Framework  | 3.14+                     |
| Database               | SQLite (default)          |
| Authentication         | DRF Token Authentication  |

---

## **Project Structure**

```
bank_management/          # Project root
├── manage.py
├── requirements.txt
├── README.md
├── bank_management/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/             # Customer auth + Bank accounts
│   ├── models.py         # BankAccount model
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── screenshots
│
└── transactions/         # Deposits, withdrawals, transfers
    ├── models.py         # Transaction model
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

---

## **Login Credentials Used**

| username | password |
|----------|----------|
| admin    | admin    |
| kawsar    | Sonali@123    |
| koushik    | Astra@123    |


## **Installation & Environment Setup**

### 1. Prerequisites

- Python 3.10 or higher
- `pip` and `venv` 

### 2. Clone / Create Project Directory

```bash
cd bank_management
```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
asgiref==3.12.1
Django==6.1.2
djangorestframework==3.18.3
sqlparse==0.6.0
tzdata==2026.5
```

### 5. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database (`db.sqlite3`) and all tables (User, Token, BankAccount, Transaction, etc.).

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts (username, email, password). This admin can access `/admin/` and all admin-only API endpoints.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Server starts at: **http://127.0.0.1:8000/**

API base URL: **http://127.0.0.1:8000/api/**

Django Admin: **http://127.0.0.1:8000/admin/**


---

## **Creating a Test User and Obtaining a Token**

### Option A – Via Registration Endpoint (Recommended)

**POST** `http://127.0.0.1:8000/api/auth/register/`

```json
{
  "username": "kawsar",
  "email": "kawsar117@gmail.com",
  "password": "Sonali@123",
  "password2": "Sonali@123",
  "first_name": "kawsar",
  "last_name": "ahmed"
}
```

Response (201):

```json
{
    "message": "Registration successful.",
    "token": "5d85794118b2938a3c6a8e4320e5ee990c989a67",
    "user": {
        "id": 1,
        "username": "kawsar",
        "email": "kawsar117@gmail.com",
        "first_name": "kawsar",
        "last_name": "ahmed"
    }
}
```

Save the `token` value. Use it in the header of all protected requests:

```
Authorization: Token 5d85794118b2938a3c6a8e4320e5ee990c989a67
```

### Option B – Via Login Endpoint (for testing)

**POST** `http://127.0.0.1:8000/api/auth/login/`

```json
{
  "username": "kawsar",
  "password": "Sonali@123"
}
```


---

## **Testing with Postman – Suggested Flow**

1. **Register** two users (User A and User B).
2. **Login** as User A → copy token.
3. **Create** a Savings account for User A.
4. **Deposit** 10000.00 into the account.
5. **Check balance** checking the balance of an account.
6. **Create** an account for User B (login as User B first).
7. **Transfer** 2000.00 from User A’s account to User B’s account number.
8. **View transaction history** for both users.
9. Try invalid operations (insufficient funds, negative amount, same-account transfer) and verify error responses.
10. Login as admin and hit the `/api/admin/*` endpoints with a is_staff = True (admin/staff user) as follows : 

    **GET** `http://127.0.0.1:8000/api/admin/customers/`
    **GET** `http://127.0.0.1:8000/api/admin/accounts/`
    **GET** `http://127.0.0.1:8000/api/admin/transactions/`

---

## **API Endpoints Execution & Testing with Postman**

All endpoints (except register & login) require the header:

```
Authorization: Token <token_here>
Content-Type: application/json
```

### 1. Authentication

| Method | Endpoint                  | Description              | Auth Required |
|--------|---------------------------|--------------------------|---------------|
| POST   | `/api/auth/register/`     | Register new customer    | No            |
| POST   | `/api/auth/login/`        | Login & get token        | No            |
| GET    | `/api/profile/`           | View own profile         | Yes           |
| PATCH  | `/api/profile/`           | Update own profile       | Yes           |


1.1 **Register new customer & getting the token**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/auth/register/

```json
{
  "username": "rajib",
  "email": "rajib@gmail.com",
  "password": "Astra@123",
  "password2": "Astra@123",
  "first_name": "koushik",
  "last_name": "rajib"
}
```

### Screenshots : ![alt text](<screenshots/1.1 New User Registration, Login& Getting Token.png>)

1.2 **Login & Getting details with Token**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/auth/login/

```json
{
  "username": "rajib",
  "password": "Astra@123"
}
```

### Screenshots : ![alt text](<screenshots/1.2 new User Successful Login.png>)

### Screenshots : ![alt text](<screenshots/1.2 new User Successful Login with Token Authentication.png>)

1.3 **View Own profile**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/auth/profile/

```json
{
  "username": "rajib",
  "password": "Astra@123"
}
```

### Screenshots : ![alt text](<screenshots/1.3 View Own Profile of an authenticated user.png>)

### Screenshots : ![alt text](<screenshots/1.3 showing the authenticated logged in profile.png>)

1.4 **Update profile**
    Method          : PATCH
    API Endpoint    : http://127.0.0.1:8000/api/auth/profile/

```json
{
  "first_name": "Koushik",
  "last_name": "Rajib",
  "email": "koushik.rajib@gmail.com"
}
```

### Screenshots : ![alt text](<screenshots/1.4 Update Profile of an authenticated user.png>)


### 2. Bank Account Management 

| Method | Endpoint                          | Description                |
|--------|-----------------------------------|----------------------------|
| GET    | `/api/accounts/`                  | List own accounts          |
| POST   | `/api/accounts/`                  | Create new account         |
| GET    | `/api/accounts/<id>/`             | View account details       |
| GET    | `/api/accounts/<id>/balance/`     | Check balance              |

2.1 **Create New Accounts**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/accounts/

```json
"account_type": "CURRENT"
```
or
```json
"account_type": "SAVINGS"
```

### Screenshots :![alt text](<screenshots/2.2 Create New Accounts.png>)

2.2 **List Own Accounts**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/accounts/

```json
{
"account_type": "CURRENT"
}
```

### Screenshots : ![alt text](<screenshots/2.1 List of Own Accounts.png>)

2.3 **View account details**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/accounts/8/

### Screenshots : ![alt text](<screenshots/2.3 View Account Details of a Particular Customer.png>)

2.4 **Check Balance**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/accounts/9/balance/

### Screenshots : ![alt text](<screenshots/2.4 Check Balance of Own Account.png>)



### 3. Transactions (Deposit / Withdraw / Transfer)

| Method | Endpoint                        | Description              |
|--------|---------------------------------|--------------------------|
| POST   | `/api/transactions/deposit/`    | Deposit money            |
| POST   | `/api/transactions/withdraw/`   | Withdraw money           |
| POST   | `/api/transactions/transfer/`   | Transfer to another acct |

3.1 **Deposit money**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/transactions/deposit/

```json
{
    "account_id": 1,
    "amount": "50000.00",
    "description": "Salary deposit"
}
```

### Screenshots : ![alt text](<screenshots/3.1 Deposit Money.png>)

3.2 **Withdraw money**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/transactions/withdraw/

```json
{
  "account_id": 1,
  "amount": "10000.00",
  "description": "ATM withdrawal"
}
```

### Screenshots : ![alt text](<screenshots/3.2 Withdraw Money.png>)

3.3 **Transfer to another account**
    Method          : POST
    API Endpoint    : http://127.0.0.1:8000/api/transactions/transfer/

```json
  "from_account_id": 8,
  "to_account_number": "201530439820",
  "amount": "5000.00",
  "description": "Payment to Brother"
```

### Screenshots : ![alt text](<screenshots/3.3 Transfer Money to Another Account.png>)


### 4. Transaction History

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| GET    | `/api/transactions/`      | Paginated history of own transactions    |

4.1 **Paginated history of own transactions**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/transactions/?type=DEPOSIT&page=1

### Screenshots : ![alt text](<screenshots/4.1 Paginated history of Own Transactions.png>)

### 5. Admin Endpoints (Staff only)

| Method | Endpoint                      | Description                |
|--------|-------------------------------|----------------------------|
| GET    | `/api/admin/customers/`       | List all customers         |
| GET    | `/api/admin/accounts/`        | List all bank accounts     |
| GET    | `/api/admin/transactions/`    | List all transactions      |

**Requires a user with `is_staff=True` or (superuser created via `createsuperuser`)**

5.1 **List All Customers**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/admin/customers/

### Screenshots : ![alt text](<screenshots/5.1 List of All Customers.png>)

### Screenshots : ![alt text](<screenshots/5.1 List of All Customers 2.png>)

5.2 **List All Bank Accounts**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/admin/accounts/

### Screenshots : ![alt text](<screenshots/5.2 List of All Accounts.png>)

5.3 **List All Transactions**
    Method          : GET
    API Endpoint    : http://127.0.0.1:8000/api/admin/transactions/

### Screenshots : ![alt text](<screenshots/5.3 List of All Transactions.png>)


### **Admin Panel Screenshots** : 

![alt text](<screenshots/Admin Panel - All Bank Accounts.png>) 

![alt text](<screenshots/Admin Panel - All Tokens.png>) 

![alt text](<screenshots/Admin Panel - All Transactions.png>) 

![alt text](<screenshots/Admin Panel - All Customers.png>)


## **Rules Implemented**

1. Every account number is unique and auto-generated.
2. Account balances can never become negative.
3. Deposits, withdrawals and transfers reject zero or negative amounts.
4. Only the account owner can perform transactions on their own accounts.
5. Customers cannot access other customers’ accounts or transaction histories.
6. Failed transactions **do not** change any balances (atomic DB transactions).
7. A successful transfer updates both balances and creates a single transaction record.
8. Transfer to the same account is forbidden.
9. Only ACTIVE accounts can receive deposits/withdrawals/transfers.


## **Notes & Best Practices Followed**

- Monetary values use `DecimalField` (never float).
- All money-moving operations are wrapped in `django.db.transaction.atomic()`.
- Custom permission class `IsOwnerOrAdmin` protects account detail/balance views.
- Token authentication is the primary auth method (SessionAuthentication also enabled for browsable API).
- Pagination is enabled globally (page size 5).

## **Future Ideas to be implemented**
● Filter transactions by date range. 
● Add daily withdrawal limits. 
● Write unit tests for deposit, withdrawal, and transfer operations. 
● Generate a downloadable account statement.

---



































































































































































































































































































































































































































































































































# **Full Project** : 

---

## **Chronological Coding Order**

1. Create project: `django-admin startproject bank_management .`
2. Create apps: `python manage.py startapp accounts` and `transactions`
3. Install DRF and add to `INSTALLED_APPS` + configure `REST_FRAMEWORK` settings
4. Define `BankAccount` model (accounts app)
5. Define `Transaction` model (transactions app)
6. Write serializers for registration, profile, accounts, deposit/withdraw/transfer
7. Implement views with proper permission classes
8. Wire up URL routes under `/api/`
9. Register models in Django admin
10. Run migrations
11. Create superuser and test endpoints
12. Finalize the README.md

---

## **Creating the project bank_management**

```bash
django-admin startproject bank_management .
```

## **Creating the accounts app (models, serializers, views, urls)**

```bash
python manage.py startapp accounts
```

### Step 1 —  preparing the bank_management/settings.py

```Python
INSTALLED_APPS = [
    # ... default Django apps ...
    # Third party
    'rest_framework',
    'rest_framework.authtoken', # for Token authentication
    # Local apps
    'accounts',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # TokenAuthentication → clients send Authorization: Token <key>
        'rest_framework.authentication.TokenAuthentication',
        # SessionAuthentication ->Django’s built-in (the default in DRF when you don’t force Token)
        'rest_framework.authentication.SessionAuthentication',
    ],

    # IsAuthenticated → every endpoint requires login by default
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny',   # temporary
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Step 2 — accounts/models.py

```python
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
    # Monetary values use `DecimalField` (never float).
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
```

```Bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Step 3 — accounts/serializers.py

```Python
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import BankAccount

# 1) Registration (used by RegisterView)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

# 2) Profile (used by ProfileView and AdminCustomerListView)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')

# 3) Bank account: create and list for customers
# Purpose: Convert models <--> JSON and perform validation.
class BankAccountSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = BankAccount
        fields = (
            'id', 
            'account_number', 
            'account_type', 
            'balance',
            'owner', 
            'owner_username', 
            'status', 
            'created_at', 
            'updated_at'
        )

        # customers shouldn’t be able to set their own following credentials : 
        read_only_fields = (
            'id', 
            'account_number', 
            'balance', 
            'owner', 
            'status',
            'created_at', 
            'updated_at'
        )

    def create(self, validated_data):
        # Owner will be set from the logged-in user later
        # For now we can accept owner in the request body (temporary)    
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


# 4) Bank account: full read-only detail for admin
class BankAccountDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = BankAccount
        fields = ('id', 'account_number', 'account_type', 'balance',
                  'owner', 'owner_username', 'owner_email', 'status',
                  'created_at', 'updated_at')
        read_only_fields = fields


# 5) Balance check
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('account_number', 'balance', 'account_type', 'status')
```

### Step 4 — accounts/views.py

```Python
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User

from .models import BankAccount
from .permissions import IsOwnerOrAdmin
# from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    BankAccountSerializer,
    BankAccountDetailSerializer,
    BalanceSerializer,
)


"""
    Order follows the customer journey:  register → login → profile → accounts → balance → admin 
"""


class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission: only owner or admin can access."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user
    

# ---------- Authentication ----------
class RegisterView(generics.CreateAPIView):
    """
    Register a new customer.
    Anyone can access this endpoint (no authentication required).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create authentication token for the new user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Registration successful.",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_201_CREATED)



class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'message': 'Login successful.',
        })


# ---------- Profile ----------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------- Bank accounts (customer) ----------
class AccountListCreateView(generics.ListCreateAPIView):
    """List own accounts or create a new account."""
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:                      # admin sees everything
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        # owner comes from the token, not from the request body
        serializer.save(owner=self.request.user)


class AccountDetailView(generics.RetrieveAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=user)


class AccountBalanceView(generics.RetrieveAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.is_staff:
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=self.request.user)


# ---------- Admin only ----------
class AdminCustomerListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminAccountListView(generics.ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountDetailSerializer
    permission_classes = [permissions.IsAdminUser]

```

### Step 5 — accounts/urls.py

```Python
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
```

### Step 6 - Connect it in the project - bank_management/urls.py :

```Python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]
```

### Test the Bank Account API in POSTMAN

Create a user first and copy the Token from the response.

```postman/body/raw > POST 
http://127.0.0.1:8000/api/auth/register/
```

```JSON
{
  "username": "kawsar",
  "email": "kawsar117@gmail.com",
  "password": "Sonali@123",
  "password2": "Sonali@123",
  "first_name": "kawsar",
  "last_name": "ahmed"
}
```
Response

```JSON
{
    "message": "Registration successful.",
    "token": "5d85794118b2938a3c6a8e4320e5ee990c989a67",
    "user": {
        "id": 1,
        "username": "kawsar",
        "email": "kawsar117@gmail.com",
        "first_name": "kawsar",
        "last_name": "ahmed"
    }
}
```
### Screenshots : ![alt text](<screenshots/1. successful user registration and token creation.png>)

```POSTMAN > Headers:
Authorization: Token 5d85794118b2938a3c6a8e4320e5ee990c989a67
Content-Type : application/json
```

Create an account with the generated TOKEN

```POSTMAN > Method : POST --> body -> raw -> json
http://127.0.0.1:8000/api/accounts/
```

```JSON
{
  "account_type": "SAVINGS"
}
```

account_number  → auto-generated
balance         → starts at 0.00
owner           → automatically set to the logged-in user
status          → defaults to ACTIVE

### Screenshots : ![alt text](<screenshots/2. new account creation via POSTMAN.png>)

## Test in Postman (in this order)

---
| # | Request & Payload | Auth Header | Expected |
| :--- | :--- | :--- | :--- |
| **1** | `POST` `/api/auth/register/` | None | 201 + token |
| **2** | `POST` `/api/auth/login/`<br>`{"username", "password"}` | None | 200 + token |
| **3** | `GET` `/api/auth/profile/` | `Token <key>` | 200 |
| **4** | `PATCH` `/api/auth/profile/`<br>`{"first_name": "Kawsar"}` | `Token <key>` | 200 |
| **5** | `POST` `/api/accounts/`<br>`{"account_type": "SAVINGS"}` | `Token <key>` | 201 |
| **6** | `GET` `/api/accounts/` | `Token <key>` | 200, only your accounts |
| **7** | `GET` `/api/accounts/1/` | `Token <key>` | 200 |
| **8** | `GET` `/api/accounts/1/balance/` | `Token <key>` | 200 |
| **9** | `GET` `/api/admin/customers/` | Customer token | 403 |
| **10** | Log in as superuser, then:<br>`GET` `/api/admin/customers/`<br>`GET` `/api/admin/accounts/` | Admin token | 200 |
---

## Creating the transactions app (models, serializers, views, urls)

```bash
python manage.py startapp transactions
```

### Step 7 —  preparing the bank_management/settings.py

```Python
INSTALLED_APPS = [
    ...
    'transactions',
]
```

### Step 8 — transactions/models.py

```bash
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import BankAccount
import uuid


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )

    transaction_id = models.CharField(max_length=36, unique=True, editable=False)
    transaction_type = models.CharField(max_length=12, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    # For deposit and withdrawal
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )
    # For transfers
    from_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='outgoing_transfers',
        null=True,
        blank=True
    )
    to_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='incoming_transfers',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions_created'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
```

```Bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Step 9 — transactions/serializers.py

```bash
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
```

### Step 10 — transactions/views.py

```bash
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
```

### Step 11 — transactions/urls.py

```bash
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
```

### Step 12 - Connect it in the project - bank_management/urls.py

```bash
urlpatterns = [
    ...
    path('api/', include('transactions.urls')),
]
```
