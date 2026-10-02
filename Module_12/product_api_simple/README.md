# Simple Product API

A simple Product API built with **Django** and **Django REST Framework (DRF)**.

## 1. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv my_env
```

Activate it on Windows:

```bash
my_env\Scripts\activate
```

Install Django and Django REST Framework:

```bash
pip install django djangorestframework
```

## 2. Run Migrations

Create migration files:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

## 3. Create a Test User

Create a test user using Django's interactive command:

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted.

## 4. Create an Authentication Token

Make sure `rest_framework.authtoken` is included in `INSTALLED_APPS`, then run:

```bash
python manage.py migrate
```

You can create a token from Django Admin:

1. Start the server.
2. Open `http://127.0.0.1:8000/admin/`
3. Log in with the test user.
4. Open **Tokens**.
5. Click **Add Token**.
6. Select the test user and save.

The generated token can be used for authenticated POST requests.

## 5. Start the Development Server

```bash
python manage.py runserver
```

API endpoint:

```text
http://127.0.0.1:8000/api/products/
```

## 6. Authentication

### GET Products

Authentication is **not required**:

```text
GET /api/products/
```

### POST Product

Authentication is required.

Add this header:

```text
Authorization: Token YOUR_TOKEN
```

Example:

```text
Authorization: Token abc123456789...
```

Then send the product data as JSON:

```json
{
    "name": "Wireless Mouse",
    "description": "A comfortable wireless mouse for everyday computer use.",
    "price": "850.00",
    "stock": 30
}
```

A successful POST returns **HTTP 201 Created**.

## 7. Pagination

The API returns products in a paginated format:

```json
{
    "count": 9,
    "next": null,
    "previous": null,
    "results": []
}
```

The API is configured to show **10 products per page**.
