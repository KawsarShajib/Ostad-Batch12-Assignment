# GhorBari — Property Rental & Management System

A Django-based property rental platform. Property owners list properties;
tenants search, request to rent, and leave reviews once accepted.

## Features

- **Authentication**: register, login, logout, profile update, two roles
  (Property Owner / Tenant) chosen at signup.
- **Property CRUD**: owners create/edit/delete their own listings only,
  enforced at both the view and middleware level.
- **Search & filters**: by location, property type, and min/max rent.
- **Rental requests**: tenants request a property; owners accept/reject;
  tenants cancel pending requests. Business rules enforced:
  - only logged-in tenants can request
  - a tenant can't request their own property
  - only the owner can accept/reject
  - no duplicate pending requests for the same property/tenant
- **Dashboards**: separate stat dashboards for owners and tenants.
- **Reviews**: 1–5 star rating + comment, only after an accepted request,
  one review per tenant per property, shown on the property detail page.
- **Custom middleware** (`accounts/middleware.py`): blocks owner-only and
  tenant-only URLs by role, redirecting with a flash message.
- **Django Admin**: Users, Properties, Rental Requests and Reviews are all
  registered with search, filters, and list-editable fields.

## Project layout

```
property_management/   # project settings & root urls
accounts/               # custom User model, auth views, middleware, dashboards
properties/              # Property model, CRUD, search/filter, listing
rentals/                 # RentalRequest & Review models, request workflow
templates/               # all HTML templates (Bootstrap 5)
static/css/style.css     # custom styling
media/                   # uploaded images (property photos, profile pics)
```

## Quick Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Login with Users created :

| Username | Password  | Notes                  |
|----------|-----------|------------------------|
| admin    | admin  | Superuser |
| kawsar    | Sonali@123   | Sample user |
| tenant    | User@123   | Sample user |
| koushik    | Owner@123   | Sample user |
| anonymous  | Tenant@123  | Sample user |

Visit :
`http://127.0.0.1:8000/` to browse properties, 
`/admin/` for the admin site, 
`/accounts/register/` to create an owner or tenant account.

###  Pagination
- Add pagination to home page and "Popular Posts" page
- Add pagination to search results page


## Project Structure

```
property_management_project/
├── accounts/  # custom User model, auth, dashboards
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py  # role-based access control
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── media/  # uploaded property & profile images
│   ├── profile_pics/
│   ├── property_gallery/
│   └── property_images/
├── properties/  # Property + PropertyImage models, CRUD, gallery
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_propertyimage.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── property_management/  # project settings & root URLs
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py  # installed apps, MAILERS, templates, media
│   ├── urls.py
│   └── wsgi.py
├── rentals/  # RentalRequest & Review models, email notifications
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── emails.py  # rental request email notifications
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/  # custom CSS
│   └── css/
│       └── style.css
├── templates/  # all HTML templates (Bootstrap 5)
│   ├── accounts/
│   │   ├── login.html
│   │   ├── owner_dashboard.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   └── tenant_dashboard.html
│   ├── properties/
│   │   ├── my_properties.html
│   │   ├── property_confirm_delete.html
│   │   ├── property_detail.html
│   │   ├── property_form.html
│   │   └── property_list.html
│   ├── rentals/
│   │   ├── my_requests.html
│   │   ├── owner_requests.html
│   │   ├── request_confirm_cancel.html
│   │   └── request_form.html
│   └── base.html
│
├── screenshots
│
│
├── .gitignore
├── README.md  # setup + feature notes
├── manage.py  # Django's command-line entry point
└── requirements.txt  # Django, Pillow

```