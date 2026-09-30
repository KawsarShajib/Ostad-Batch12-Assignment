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
