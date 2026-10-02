# Simple Product API

A simple Product API built with **Django** and **Django REST Framework (DRF)**.

## 1. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install Django and Django REST Framework:

```bash
pip install django
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

The API is configured to show **5 products per page**.


# 8. Final Project Structure

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


# 9. SCREENSHOTS : 

## Screenshot of : admin panel with auth token

![alt text](<Screenshots/admin panel with auth token.png>)

## Screenshot of : admin panel with products

![alt text](<Screenshots/admin panel with products.png>)

## Screenshot of : empty product list with GET without AUTHENTICATION

![alt text](<Screenshots/Empty Product List with GET WITHOUT AUTHENTICATION.png>)

## Screenshot of : authentication error on creating new products without token

![alt text](<Screenshots/authentication error on creating new products without token authentication.png>)

## Screenshot of : creating new products using POST method with TOKEN AUTH

![alt text](<Screenshots/creating new products using POST method with token authentication.png>)

## Screenshot of : use of TOKEN AUTHENTICATION 

![alt text](<Screenshots/use of token authentication.png>)

## Screenshot of : valiadation error on adding a product with an empty name

![alt text](<Screenshots/validation error on adding a product with an empty name.png>)

## Screenshot of : valiadation error on adding a product with an empty price

![alt text](<Screenshots/validation error on adding a product with an empty price.png>)

## Screenshot of : valiadation error on adding a product with decimal stock

![alt text](<Screenshots/validation error on adding a product with decimal stock.png>)

## Screenshot of : valiadation error on adding a product with negative price

![alt text](<Screenshots/validation error on adding a product with negative price.png>)

## Screenshot of : valiadation error on adding a product with negative stock

![alt text](<Screenshots/validation error on adding a product with negative stock.png>)

## Screenshot of : screenshot showing second page of products
![alt text](<Screenshots/screenshot showing second page of products.png>)