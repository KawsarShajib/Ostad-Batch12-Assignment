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

    'PAGE_SIZE': 10,
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
```

---
