# Campus Lost & Found System

A Django web app for reporting and finding lost/found items on campus.

## Features implemented

- **Authentication**: register, login, logout 
- **Reports CRUD**: create, view (list + detail), edit, and delete reports. 
- **Fields**: item name, type (Lost/Found), category, description, location, date, contact info, optional image.
- **Search & filter**: by item name/description/location text, category, type, and status 
- **Status**: Active / Resolved. Owners can mark their own report "Resolved" 
- **Templates**: `base.html` (navbar/layout) extended by `home.html`, `reports.html`, `report_detail.html`, `report_form.html` (create+edit), `report_confirm_delete.html`, `login.html`, `register.html`, `my_reports.html`.
- **Custom middleware** (`reports/middleware.py`): logs `User | Method | Path | Time` to the terminal for every request.
- **Django messages**: success/info messages shown after register, login/logout, create, update, delete, and resolve actions.

## Project layout

```
Assignment Module - 08/
│
├── campus_lostfound/  
│   └── project settings, urls, wsgi/asgi
│
├── media
│   └── report_images/
│
├── reports/
│   ├── migrations/....
│   ├── __init__.p
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── static/css/style.css
│
├── templates/ 
│   └── base.html
│   └── home.html
│   └── login.html
│   └── my_reports.html
│   └── register.html
│   └── report_confirm_delete.html
│   └── report_detail.html
│   └── report_form.html
│   └── reports.html
│
├── db.sqlite3
├── manage.py
├── project_structure.png
├── README.md
└── requirements.txt


```

## Setup & run

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (SQLite db is created automatically)
python manage.py migrate

# 4. (Optional) Create an admin superuser
python manage.py createsuperuser

# OR you can replace the db.sqlite3 file 
# (with login credentials as username=kawsar, password=123)


# 5. Run the dev server
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` — home page
- `http://127.0.0.1:8000/register/` — create an account
- `http://127.0.0.1:8000/reports/` — browse/search all reports
- `http://127.0.0.1:8000/my-reports/` — manage your own reports
- `http://127.0.0.1:8000/admin/` — Django admin (after creating a superuser)

While the server runs, watch the terminal — every request logs a line like:

```
User: kawsar | Method: POST | Path: /reports/create/ | Time: 0.08s
```


