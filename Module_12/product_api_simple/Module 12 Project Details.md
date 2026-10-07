# Simple Product API

A beginner-friendly Django REST Framework project for a small online shop.

The API allows:

* Anyone to view available products.
* Authenticated users to add new products.
* Invalid product information to be rejected.
* Products to be returned in a paginated response.
* Token authentication using Django REST Framework's built-in `TokenAuthentication`.

Editing, deleting, shopping carts, payments, and frontend design are outside the scope of this assignment.

---

# 1. Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* Token Authentication

---

# 2. Project Structure

The project will contain:

```text
shop_project/
│
├── manage.py
│
├── shop_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── products/
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    └── tests.py
```

---

# 3. Creating and activating a Virtual Environment

```bash
python -m venv venv
source venv\Scripts\activate
```

---

# 4. Install Django, Django REST Framework and additional packages

Install Django:

```bash
pip install django
pip install djangorestframework 
pip install markdown            # Markdown support for the browsable API 
pip install django-filter       # Filtering support
```

Save list of all installed packages for reference : 

```bash
pip freeze > requirements.txt
```

---

# 5. Create the Django Project

```bash
django-admin startproject shop_project .
```

The dot (`.`) is important because it creates the project in the current folder.

---

# 6. Create the Products App

Create an app named `products`:

```bash
python manage.py startapp products
```

---

# 7. Configure Installed Apps

```python
INSTALLED_APPS = [
    ....
    'rest_framework',
    'rest_framework.authtoken',

    'products',
]
```

---

# 8. Configure REST Framework in shop_project/settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 5,
}
```

---

# 9. Create the Product Model in products/models.py

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
```

---

# 10. Create and apply the Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the required database tables in the default SQLite database.

---

# 11. Create the Product Serializer in products/serializers.py

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )

        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value

    def validate_stock(self, value): 
        if value < 0: 
            raise serializers.ValidationError( 
                "Stock cannot be negative." 
            ) 
        if not isinstance(value, int): 
            raise serializers.ValidationError( 
                "Stock must be a whole number." 
            ) 
        return value
```

---

# 12. Create the API View in products/views.py

```python
from rest_framework.generics import ListCreateAPIView

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
```

---

# 13. Create Product URLs in products/urls.py

```python
from django.urls import path
from .views import ProductListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
```

---

# 14. Connect App URLs to Project URLs in shop_project/urls.py

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    # the product API will be available at: /api/products/
    # Therefore: 
    # GET /api/products/    and
    # POST /api/products/   will use the same endpoint.
]
```

---


# 15. Configure Token Authentication

Token authentication is already enabled in: shop_project/settings.py

because we added:

```python
'rest_framework.authtoken',
```

and:

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
],
```

The permission is:

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
],
```

Therefore:

| Request | Authentication |
| ------- | -------------- |
| GET     | Not required   |
| POST    | Required       |

---

# 16. Create a SuperUser

```bash
python manage.py createsuperuser
```

---

# 17. Generate an Authentication Token

Option 1 : Use Django Admin

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(username='admin')

token, created = Token.objects.get_or_create(user=user)

print(token.key)
```

Replace 'admin'  with the username.

The terminal will display a token like:

```text
fd1081bbd500b16d3fd4bee087da35e680ceca77
```

Copy this token for future use in postman, etc.

Exit the shell:

```python
exit()
```

Option 2 : Use Django Admin

Start the Django shell. Go to:

```bash
http://127.0.0.1:8000/admin/
```
Then:

```bash
Tokens → Add Token
```


Option 3 : Create a Token API Endpoint

A more realistic API approach is to create an endpoint such as:
```bash
POST /api/token/
```
where the user sends their username and password, and the API returns their token.

DRF provides obtain_auth_token specifically for this purpose.

Step 1 — Modify shop_project/urls.py

```bash
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),

    path('api/token/', views.obtain_auth_token),
]
```

Now DRF provides:

```bash
        POST /api/token/
```

Step 2 — Use Postman

Create a request:

```bash
    POST  http://127.0.0.1:8000/api/token/
```
Choose:

```bash
    Body → x-www-form-urlencoded
```
Add:

```bash
    Key	        Value
    username	your username
    password	your password
```
---


# 18. Start the Development Server

```bash
python manage.py runserver
```

---

# 19. Test GET Without Authentication

Open this URL in the browser. We do NOT need a token.

```text
http://127.0.0.1:8000/api/products/
```

If there are no products yet, the response should be a paginated response similar to:

```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

This satisfies the requirement that an empty product list must still be returned inside the paginated response.

---

# 20. Add a Product Using POST

A visitor cannot create a product without authentication. We must include the token in the request header.

The header must be:

```text
Authorization: Token MY_TOKEN
```

---

# 21. POST Request Data

Send:

```json
{
    "name": "Notebook",
    "description": "A notebook with 100 pages.",
    "price": "120.00",
    "stock": 25
}
```

Notice that we do not include:

```text
id
```

because Django generates id automatically.

---

# 22. Testing With Postman

We can use Postman to test the API. Create a new request.

Choose:

```text
POST
```

Enter:

```text
http://127.0.0.1:8000/api/products/
```

Go to:

```text
Headers
```

Add:

```text
Key: Authorization
Value: Token MY_TOKEN
```

Replace `MY_TOKEN` with actual token.

Then go to:

```text
Body → raw → JSON
```

Enter:

```json
{
    "name": "Mobile",
    "description": "Iphone 18 pro",
    "price": "3000.00",
    "stock": 50
}

```

Send the request.

---

# 23. Expected Successful POST Response

A successful request should return:

```text
HTTP 201 Created
```

with a response similar to:

```json
{
    "id": 1,
    "name": "Notebook",
    "description": "A notebook with 100 pages.",
    "price": "120.00",
    "stock": 25
}
```

The ID:

```text
1
```

was automatically generated by Django.

---

# 24. Test GET Again

Now open:

```text
http://127.0.0.1:8000/api/products/
```

We should receive:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Notebook",
            "description": "A notebook with 100 pages.",
            "price": "120.00",
            "stock": 25
        }
    ]
}
```

GET works without a token because visitors are allowed to browse products.

---

# 25. Test POST Without a Token

Try to create a product without including:

```text
Authorization: Token MY_TOKEN
```

For example:

```json
{
    "name": "Pen",
    "description": "A blue ballpoint pen.",
    "price": "20.00",
    "stock": 50
}
```

The request should be rejected. The response will normally be:

```text
HTTP 401 Unauthorized
```

with an authentication error. This confirms that visitors cannot add products.

---

# 25. Test Invalid Product Name

Try:

```json
{
    "name": "",
    "description": "A notebook.",
    "price": "120.00",
    "stock": 25
}
```

The request should fail with a validation error similar to:

```json
{
    "name": [
        "Product name cannot be empty."
    ]
}
```

---

# 26. Test Invalid Price

Try:

```json
{
    "name": "Notebook",
    "description": "A notebook.",
    "price": "0.00",
    "stock": 25
}
```

The request should fail with:

```json
{
    "price": [
        "Price must be greater than zero."
    ]
}
```

The same applies to a negative price.

For example:

```json
"price": "-50.00"
```

is invalid.

---

# 27. Test Invalid Stock

Try:

```json
{
    "name": "Notebook",
    "description": "A notebook.",
    "price": "120.00",
    "stock": -5
}
```

This should be rejected because stock cannot be negative.

A decimal stock value such as:

```json
"stock": 5.5
```

should also be rejected because stock must be a whole number.

---

# 28. Test Pagination

The API uses:

```python
'PAGE_SIZE': 5
```

Therefore, if there are more than 5 products, the API will divide them into pages.

First page:

```text
GET /api/products/
```

Second page:

```text
GET /api/products/?page=2
```

The response contains:

```json
{
    "count": 6,
    "next": "http://127.0.0.1:8000/api/products/?page=2",
    "previous": null,
    "results": [
        ...
    ]
}
```

The exact URLs can vary depending on the server configuration.

---

# 29. Final Project Structure

After completing the project, our structure should look similar to:

```text
product_api_simple/
│
├── products/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── Screenshots/
│
├── shop_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── venv/
│
├── db.sqlite3
│
├── manage.py
│
├── README.md
├── requirements.txt


```

---


# 30. PROJECT SCREENSHOTS : 

See README.md file/Screenshots directory

---

# 31. Complete Project Files

## products/models.py

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
```

---

## products/serializers.py

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )

        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value
```

---

## products/views.py

```python
from rest_framework.generics import ListCreateAPIView
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
```

---

## products/urls.py

```python
from django.urls import path
from .views import ProductListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
```

---

## shop_project/urls.py

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('products.urls')),
]
```

---

## shop_project/settings.py

Make sure these applications are included:

```python
INSTALLED_APPS = [
    ....
    'rest_framework',
    'rest_framework.authtoken',
    'products',
]
```

And make sure this REST Framework configuration exists:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 5,
}
```

---

# 32. Complete Command Sequence

For convenience, the main commands are:

## Install Dependencies

```bash
mkdir product_api
cd product_api

python -m venv venv

venv\Scripts\activate

pip install django
pip install djangorestframework
# pip install djangorestframework-authtoken

```

## Create Project

```bash
django-admin startproject shop_project .

python manage.py startapp products
```

## Create database tables

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create test user

```bash
python manage.py createsuperuser
```

## Generate token

```bash
python manage.py shell
```

Then:

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(username='admin')

token, created = Token.objects.get_or_create(user=user)

print(token.key)
```

Exit:

```python
exit()
```

## Start server

```bash
python manage.py runserver
```

---

# 33. API Summary

| Method | URL              | Authentication | Purpose       |
| ------ | ---------------- | -------------- | ------------- |
| GET    | `/api/products/` | Not required   | View products |
| POST   | `/api/products/` | Required       | Add a product |

---

# 34. Example Product

### Request

```json
{
    "name": "Notebook",
    "description": "A notebook with 100 pages.",
    "price": "120.00",
    "stock": 25
}
```

### Response

```json
{
    "id": 1,
    "name": "Notebook",
    "description": "A notebook with 100 pages.",
    "price": "120.00",
    "stock": 25
}
```

Status:

```text
201 Created
```

---

# 35. Assignment Requirements Checklist

## Project

* [x] Django project named `shop_project`
* [x] App named `products`
* [x] Django REST Framework installed
* [x] SQLite database used

## Product Model

* [x] Automatically generated ID
* [x] Name with maximum 100 characters
* [x] Description
* [x] Price with two decimal places
* [x] Stock
* [x] Migrations created and applied

## Serializer

* [x] `ProductSerializer`
* [x] Uses `ModelSerializer`
* [x] Includes all five fields
* [x] ID is read-only
* [x] Empty name rejected
* [x] Price must be greater than zero
* [x] Stock must be a whole number
* [x] Negative stock rejected
* [x] Useful validation messages

## GET API

* [x] `GET /api/products/`
* [x] Anyone can view products
* [x] Products ordered by ID
* [x] Paginated response
* [x] Empty results returned when no products exist

## POST API

* [x] `POST /api/products/`
* [x] Uses `ListCreateAPIView`
* [x] Authentication required
* [x] Valid product saved
* [x] Generated ID returned
* [x] HTTP 201 Created returned

## Authentication

* [x] DRF TokenAuthentication
* [x] Test user created
* [x] Token generated
* [x] GET allowed without token
* [x] POST requires token
* [x] `IsAuthenticatedOrReadOnly` used
* [x] `Authorization: Token MY_TOKEN` supported

---

# 36. Final Result

The completed API provides the following basic workflow:

```text
Visitor
   │
   │ GET /api/products/
   ▼
View Products
```

An authenticated user can:

```text
Authenticated User
       │
       │ POST /api/products/
       │ Authorization: Token MY_TOKEN
       ▼
Validate Product
       │
       ├── Invalid → Error Response
       │
       └── Valid
             │
             ▼
        Save Product
             │
             ▼
       201 Created
```

Therefore, the project satisfies the assignment goal:

**Visitors can browse products, authenticated users can add valid products, and invalid product information is rejected.**



