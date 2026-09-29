# Campus Lost & Found — Build It Yourself, Step by Step (Full Code)

This guide builds the entire project from an empty folder to a fully working app, one file at a time, in the order you'd actually type it. Every code block is the **complete, real file** — copy it in exactly as shown. After each file, there's a plain-English explanation of what you just typed and why.

> Total build time: ~45–60 minutes for a first-timer, typing everything out.

---

## Step 0 — Install Python and check it works

You need Python 3.10 or newer.

```bash
python --version
```

If that fails, try `python3 --version`. Either is fine — just use whichever works for every command below.

---

## Step 1 — Create the project folder and a virtual environment

```bash
mkdir campus_lostfound
cd campus_lostfound
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**Why:** a virtual environment is an isolated set of Python packages just for this project, so it doesn't clash with other projects on your machine. You'll know it's active because your prompt shows `(venv)` at the start.

---

## Step 2 — Install Django and Pillow

```bash
pip install "Django>=5.0,<6.0" "Pillow>=10.0"
```

**Why Pillow?** Django's `ImageField` (used for report photos) needs the Pillow library under the hood to process images — without it, migrations involving `ImageField` fail.

Save what you installed so anyone else can reproduce it:
```bash
pip freeze > requirements.txt
```
Or just create it by hand:

```text
Django>=5.0,<6.0
Pillow>=10.0
```
Save this as `requirements.txt` in the `campus_lostfound` folder.

---

## Step 3 — Start the Django project

```bash
django-admin startproject campus_lostfound .
```

Notice the trailing `.` — it tells Django "create the project files right here" instead of nesting everything in an extra subfolder. You'll now have:

```
campus_lostfound/          ← this is your working folder (contains manage.py)
├── manage.py
└── campus_lostfound/       ← this is the PROJECT config package (same name, that's normal)
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

Having two folders with the same name is confusing at first but completely normal — the outer one is just "the repo," the inner one is Django's generated settings package.

**`manage.py`** — you'll run every Django command through this file (`python manage.py <something>`). You never need to edit it. For reference, here's what Django generates:

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_lostfound.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

**`wsgi.py`** and **`asgi.py`** — entry points a real production web server would use to talk to your app. You won't touch these; shown here just so you recognize them:

```python
# campus_lostfound/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_lostfound.settings')

application = get_wsgi_application()
```

```python
# campus_lostfound/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_lostfound.settings')

application = get_asgi_application()
```

Quick sanity check — this should start a server (even though it's empty so far):
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` — you should see Django's default "the install worked" rocket page. Stop the server with `Ctrl+C` and continue.

---

## Step 4 — Start the `reports` app

A Django **project** is the whole site; an **app** is one feature area. We'll put almost everything — reports AND the auth pages — into a single app called `reports`.

```bash
python manage.py startapp reports
```

This creates:
```
reports/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```
We'll fill in `models.py`, `views.py`, `admin.py`, and add three files Django *doesn't* auto-create: `urls.py`, `forms.py`, and `middleware.py`.

Also create the folders for HTML pages and CSS, which live at the project's top level (not inside the app):

```bash
mkdir -p templates
mkdir -p static/css
```

---

## Step 5 — Configure `settings.py`

Open `campus_lostfound/settings.py` and replace its contents with this:

```python
"""
Django settings for campus_lostfound project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep this secret in production (use environment variables)!
SECRET_KEY = 'django-insecure-change-this-secret-key-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware: logs user, request method, path, and processing time
    'reports.middleware.RequestLogMiddleware',
]

ROOT_URLCONF = 'campus_lostfound.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'campus_lostfound.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (user-uploaded report images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

**Line-by-line, the parts that matter:**

| Setting | What it does |
|---|---|
| `INSTALLED_APPS` | Every app Django loads. We added `'reports'` at the bottom. `django.contrib.auth` is what gives us User accounts, login, logout for free. |
| `MIDDLEWARE` | A list of classes that run on every request, top to bottom (and back up in reverse for the response). We appended our own `reports.middleware.RequestLogMiddleware` — we'll write that class in Step 9. |
| `TEMPLATES` → `DIRS` | Tells Django to also look in a top-level `templates/` folder (not just inside each app) for HTML files. |
| `DATABASES` | Uses SQLite — a single file (`db.sqlite3`), zero setup, perfect for learning. |
| `STATIC_URL` / `STATICFILES_DIRS` | Where CSS/JS files live and what URL prefix serves them. |
| `MEDIA_URL` / `MEDIA_ROOT` | Where **uploaded** files (report photos) get saved and served from — different from `static/`, which is for files *you* wrote. |
| `LOGIN_URL = 'login'` | If a logged-out user visits a page that requires login, Django sends them to the URL named `'login'` (we'll define that name in Step 11). |

---

## Step 6 — Define the database model

Open `reports/models.py` and replace its contents:

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Report(models.Model):
    TYPE_LOST = 'Lost'
    TYPE_FOUND = 'Found'
    TYPE_CHOICES = [
        (TYPE_LOST, 'Lost'),
        (TYPE_FOUND, 'Found'),
    ]

    CATEGORY_CHOICES = [
        ('Documents', 'Documents'),
        ('Electronics', 'Electronics'),
        ('Accessories', 'Accessories'),
        ('Clothing', 'Clothing'),
        ('Keys', 'Keys'),
        ('Bags', 'Bags'),
        ('Others', 'Others'),
    ]

    STATUS_ACTIVE = 'Active'
    STATUS_RESOLVED = 'Resolved'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    item_name = models.CharField(max_length=150)
    report_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField(help_text="Date the item was lost or found")
    contact_info = models.CharField(max_length=150, help_text="Phone number or email")
    image = models.ImageField(upload_to='report_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.report_type}] {self.item_name} ({self.status})"

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})

    def is_owner(self, user):
        return self.owner_id == user.id
```

**What's happening here, field by field:**

- **`owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')`** — this is the single most important line in the whole project. It creates a link from every `Report` row to exactly one `User` row. `on_delete=models.CASCADE` means "if that user is deleted, delete their reports too." `related_name='reports'` means you could later write `some_user.reports.all()` to get all of someone's reports.
- **`CharField` vs `TextField`** — `CharField` needs a `max_length` and is meant for short text (names, locations). `TextField` has no length limit and is for long free text (the description).
- **`choices=TYPE_CHOICES`** — restricts the field to a fixed list of options. Each entry is a `(stored_value, human_readable_label)` pair. Django auto-renders these as a dropdown (`<select>`) in forms.
- **`ImageField(upload_to='report_images/', blank=True, null=True)`** — an optional photo. `blank=True` = optional in forms; `null=True` = the database column is allowed to be empty. `upload_to` says where inside `MEDIA_ROOT` uploaded files get saved.
- **`auto_now_add=True`** vs **`auto_now=True`** — the first sets the timestamp once, when the row is first created (`created_at`); the second updates it every single time the row is saved (`updated_at`).
- **`class Meta: ordering = ['-created_at']`** — newest reports show up first by default, everywhere, without any view needing to say so.
- **`is_owner(self, user)`** — a small helper method we wrote by hand. We'll call `report.is_owner(request.user)` constantly in views to check permissions, instead of repeating `report.owner_id == request.user.id` everywhere.

---

## Step 7 — Create and apply the migration

Whenever you write or change a model, Django needs two commands:

```bash
python manage.py makemigrations reports
```
This scans `models.py`, notices the new `Report` model, and writes a migration file (a set of instructions for changing the database) into `reports/migrations/0001_initial.py`. You'll see output like:
```
Migrations for 'reports':
  reports/migrations/0001_initial.py
    + Create model Report
```

```bash
python manage.py migrate
```
This actually applies all pending migrations — both ours and Django's built-in ones (for users, sessions, admin, etc.) — creating real tables inside `db.sqlite3`.

**Rule of thumb you'll use for the rest of your Django life:** change `models.py` → `makemigrations` → `migrate`. Skip a step and you'll get errors like `no such table` or `you have unapplied migrations`.

---

## Step 8 — Register the model with Django admin

Open `reports/admin.py`:

```python
from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'report_type', 'category', 'status', 'owner', 'date', 'created_at')
    list_filter = ('report_type', 'category', 'status')
    search_fields = ('item_name', 'description', 'location')
```

**Why:** this one small file unlocks a full admin dashboard at `/admin/` — a searchable, filterable table of every report, with built-in edit/delete — without you writing a single view or template for it. `list_display` controls the columns shown; `list_filter` adds sidebar filters; `search_fields` adds a search box.

Also confirm `reports/apps.py` looks like this (Django generated it, no changes needed, shown for completeness):

```python
from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
```

Create an admin login so you can actually visit `/admin/` later:
```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password).

---

*(Continued in the next section: forms, middleware, views, URLs, and every template — Step 9 onward.)*
# Part 2 — Forms, Middleware, Views, URLs

*(Continues from Part 1. By now you have: project + app created, settings configured, `Report` model migrated, admin registered.)*

---

## Step 9 — Write `reports/middleware.py` (new file)

This file doesn't exist yet — create it inside the `reports/` folder:

```python
import time
import logging

logger = logging.getLogger('reports.request_logger')


class RequestLogMiddleware:
    """
    Custom middleware that logs, for every request:
      - User (username or 'Anonymous')
      - Request Method (GET, POST, etc.)
      - URL/Path
      - Time taken to process the request (seconds)

    Example terminal output:
      User: Rahim | Method: POST | Path: /reports/create/ | Time: 0.08s
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        user = request.user if request.user.is_authenticated else 'Anonymous'

        log_message = (
            f"User: {user} | Method: {request.method} | "
            f"Path: {request.path} | Time: {duration:.2f}s"
        )

        # Print to terminal (console) as requested, and also log it properly.
        print(log_message)
        logger.info(log_message)

        return response
```

**How middleware actually works:** Django creates *one instance* of this class when the server starts (that's `__init__`, which just stores a reference to "the next thing in the chain," `get_response`). Then, for **every single request**, Django calls `__call__(request)`.

- Anything written **before** `response = self.get_response(request)` runs *before* your view function executes.
- `self.get_response(request)` is the line that actually triggers the URL routing → view → template process.
- Anything written **after** that line runs *after* the view has produced its response, but before it's sent to the browser.

That's why we start the timer before `get_response` and read it after — we're measuring exactly how long the view took. You already registered this class in `settings.py`'s `MIDDLEWARE` list back in Step 5, so it's already wired in — you don't call it manually anywhere.

---

## Step 10 — Write `reports/forms.py` (new file)

Forms turn raw HTML `<input>` submissions into validated Python data, and can also auto-generate HTML fields from a model.

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Report


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ReportForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Report
        fields = [
            'item_name', 'report_type', 'category', 'description',
            'location', 'date', 'contact_info', 'image',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Student ID Card'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                   'placeholder': 'Describe the item in detail...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Library, 2nd Floor'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone or email'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReportSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search',
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by item name...'}))
    report_type = forms.ChoiceField(required=False, label='Type',
                                     choices=[('', 'All')] + Report.TYPE_CHOICES,
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ChoiceField(required=False, label='Category',
                                  choices=[('', 'All')] + Report.CATEGORY_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(required=False, label='Status',
                                choices=[('', 'All')] + Report.STATUS_CHOICES,
                                widget=forms.Select(attrs={'class': 'form-select'}))
```

**Three forms, three purposes:**

1. **`RegisterForm`** — instead of writing a username/password form from scratch, we extend Django's built-in `UserCreationForm` (which already handles password confirmation and hashing safely) and just add an `email` field on top. The `__init__` override loops over every field and adds Bootstrap's `form-control` CSS class, so it looks consistent without repeating `attrs={'class': ...}` on each field individually.

2. **`ReportForm`** is a **`ModelForm`** — instead of manually declaring 8 fields, we point it at the `Report` model and list which fields to expose: `fields = ['item_name', 'report_type', ...]`. Django reads each field's type from the model and auto-generates the right HTML input. Two fields are **deliberately excluded**: `owner` (set in the view from whoever's logged in — never something a user should type in themselves) and `status` (only changed through the dedicated "Resolve" action, covered in Step 12).

3. **`ReportSearchForm`** is a plain `forms.Form` (not tied to a model) — used only for the search bar. Every field has `required=False` so an empty search shows everything. `choices=[('', 'All')] + Report.TYPE_CHOICES` prepends a blank "All" option onto the model's real choices.

---

## Step 11 — Write `reports/views.py`

Replace the contents of the auto-generated `reports/views.py`:

```python
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

from .forms import RegisterForm, ReportForm, ReportSearchForm
from .models import Report


def home(request):
    """Landing page: shows a few recent active reports and quick stats."""
    recent_reports = Report.objects.filter(status=Report.STATUS_ACTIVE)[:6]
    context = {
        'recent_reports': recent_reports,
        'total_active': Report.objects.filter(status=Report.STATUS_ACTIVE).count(),
        'total_resolved': Report.objects.filter(status=Report.STATUS_RESOLVED).count(),
    }
    return render(request, 'home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


def report_list(request):
    """Read: view all reports, with search/filter support."""
    search_form = ReportSearchForm(request.GET or None)
    reports = Report.objects.all()

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q')
        report_type = search_form.cleaned_data.get('report_type')
        category = search_form.cleaned_data.get('category')
        status = search_form.cleaned_data.get('status')

        if q:
            reports = reports.filter(
                Q(item_name__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q)
            )
        if report_type:
            reports = reports.filter(report_type=report_type)
        if category:
            reports = reports.filter(category=category)
        if status:
            reports = reports.filter(status=status)

    paginator = Paginator(reports, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'reports.html', context)


def report_detail(request, pk):
    """Read: view a single report's details."""
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'report_detail.html', {'report': report})


@login_required
def report_create(request):
    """Create: logged-in users create a report tied to themselves."""
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = request.user
            report.save()
            messages.success(request, "Report created successfully!")
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {'form': form, 'is_edit': False})


@login_required
def report_update(request, pk):
    """Update: only the owner may edit their report."""
    report = get_object_or_404(Report, pk=pk)
    if not report.is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to edit this report.")

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated successfully!")
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm(instance=report)
    return render(request, 'report_form.html', {'form': form, 'is_edit': True, 'report': report})


@login_required
def report_delete(request, pk):
    """Delete: only the owner may delete their report."""
    report = get_object_or_404(Report, pk=pk)
    if not report.is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to delete this report.")

    if request.method == 'POST':
        report.delete()
        messages.success(request, "Report deleted successfully!")
        return redirect('my_reports')
    return render(request, 'report_confirm_delete.html', {'report': report})


@login_required
@require_POST
def report_resolve(request, pk):
    """Owner marks their own report as Resolved."""
    report = get_object_or_404(Report, pk=pk)
    if not report.is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to modify this report.")

    report.status = Report.STATUS_RESOLVED
    report.save(update_fields=['status', 'updated_at'])
    messages.success(request, "Report marked as resolved!")

    next_url = request.POST.get('next')
    if next_url == 'my_reports':
        return redirect('my_reports')
    return redirect('report_detail', pk=report.pk)


@login_required
def my_reports(request):
    """Show only the logged-in user's own reports."""
    reports = Report.objects.filter(owner=request.user)
    paginator = Paginator(reports, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'my_reports.html', {'page_obj': page_obj})
```

**Going through this function by function:**

- **`home`** — no login required. Pulls the 6 newest active reports (`[:6]` slices the queryset, which Django translates into `LIMIT 6` in SQL) plus two counts for the stat cards.

- **`register`** — if you're already logged in, bounce to home. Otherwise: `GET` shows a blank form; `POST` validates it, and if valid, `form.save()` (inherited from `UserCreationForm`) creates the actual `User` row with a properly hashed password. `login(request, user)` immediately logs them in — no separate login step needed after registering.

- **`CustomLoginView` / `CustomLogoutView`** — rather than write login/logout from scratch, we reuse Django's built-in `LoginView`/`LogoutView` (they already handle password checking, sessions, redirect-after-login, etc.) and just override small bits: which template to use, and firing a `messages.success(...)` / `messages.info(...)` at the right moment.

- **`report_list`** — this is the search/filter engine. `ReportSearchForm(request.GET or None)` binds the form to whatever's in the URL's query string (e.g. `?q=ID+Card&report_type=Lost`). `Q(...)` objects combined with `|` mean "match ANY of these fields"; each separate `.filter(...)` call chains together as AND. `Paginator(reports, 9)` splits the results into pages of 9.

- **`report_detail`** — the simplest view: fetch one report by primary key or return a 404 if it doesn't exist (`get_object_or_404`).

- **`report_create`** — guarded by `@login_required` (redirects to `/login/` if you're not signed in). The key trick: `form.save(commit=False)` builds the `Report` object in memory *without* writing to the database yet, so we can attach `report.owner = request.user` first, then call `report.save()` ourselves. `request.FILES` is passed alongside `request.POST` specifically because this form can include an uploaded image — file uploads travel separately from regular form fields.

- **`report_update`** — same GET/POST pattern as create, but starts with a permission check: `if not report.is_owner(request.user): return HttpResponseForbidden(...)`. This runs on the server, so it can't be bypassed by hiding a button in the browser — someone would have to literally break Django's request handling to get around it.

- **`report_delete`** — same ownership check. On `GET`, shows a confirmation page instead of deleting immediately (never delete on a simple page visit — a stray link or crawler bot could trigger it). Only an actual `POST` (the confirm button) deletes.

- **`report_resolve`** — stacked decorators: `@login_required` then `@require_POST`. `require_POST` means this view *only* accepts POST requests — visiting its URL directly with a browser address bar (which sends GET) gets rejected. That's intentional: resolving should only happen by clicking the button, which submits a form.

- **`my_reports`** — filters to `owner=request.user`, so you only ever see your own reports here (as opposed to `report_list`, which shows everyone's).

---

## Step 12 — Write `reports/urls.py` (new file)

Create this file inside `reports/`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Reports CRUD + list/search
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/edit/', views.report_update, name='report_update'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    path('reports/<int:pk>/resolve/', views.report_resolve, name='report_resolve'),

    # Own reports
    path('my-reports/', views.my_reports, name='my_reports'),
]
```

**What's going on:**
- `path('reports/<int:pk>/edit/', views.report_update, name='report_update')` — `<int:pk>` is a **URL converter**: it captures a number from the address (e.g. `5` from `/reports/5/edit/`) and passes it into the view as the `pk` keyword argument.
- `.as_view()` — class-based views (like `CustomLoginView`) need this conversion to become a plain function Django's router can call; regular function-based views (`views.home`) don't.
- `name='...'` — gives each URL a permanent nickname. Templates and views reference URLs by this name (`{% url 'report_detail' report.pk %}`, `redirect('report_detail', pk=report.pk)`) instead of hardcoding the path string — so if you ever change a path, nothing breaks elsewhere.

Now open the **project-level** `campus_lostfound/urls.py` (from Step 3) and replace it:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
```

**Why two `urls.py` files?** The project-level one is the single entry point Django checks first; `include('reports.urls')` hands off everything to the app's own URL file. This separation matters once a project grows to have multiple apps — each gets its own `urls.py`, and the project file just includes all of them. The `static(...)` lines at the bottom are only needed in development (`DEBUG = True`) — they tell Django to personally serve uploaded images and CSS files, something a real production server would normally handle instead.

---

*(Continued in Part 3: every HTML template, then running and testing the finished app.)*
# Part 3 — Templates, Styling, and Running the Finished App

*(Continues from Part 2. By now: models, admin, middleware, forms, views, and URLs are all done. Only the HTML pages are left.)*

All template files go in the top-level `templates/` folder you created in Step 4 (**not** inside `reports/`).

---

## Step 13 — `templates/base.html` (the shared layout, build this first)

Every other page extends this one, so build it first.

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Campus Lost & Found{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand fw-bold" href="{% url 'home' %}">🎒 Campus Lost & Found</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'report_list' %}">All Reports</a></li>
                {% if user.is_authenticated %}
                <li class="nav-item"><a class="nav-link" href="{% url 'report_create' %}">+ New Report</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'my_reports' %}">My Reports</a></li>
                {% endif %}
            </ul>
            <ul class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                <li class="nav-item"><span class="nav-link disabled">Hi, {{ user.username }}</span></li>
                <li class="nav-item">
                    <form method="post" action="{% url 'logout' %}" class="d-inline">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-outline-light btn-sm mt-1">Logout</button>
                    </form>
                </li>
                {% else %}
                <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Login</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'register' %}">Register</a></li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

<div class="container">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}

    {% block content %}{% endblock %}
</div>

<footer class="text-center text-muted py-4 mt-5">
    <small>&copy; {% now "Y" %} Campus Lost & Found System</small>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Key template concepts here, used everywhere from now on:**
- `{% load static %}` + `{% static 'css/style.css' %}` — tells Django to generate the correct URL for our CSS file based on `STATIC_URL`.
- `{% block title %}...{% endblock %}` and `{% block content %}{% endblock %}` — these are **placeholders**. Child templates fill them in via `{% extends "base.html" %}` + their own `{% block content %}...{% endblock %}`. Anything outside a block in a child template is ignored.
- `{% url 'home' %}` — generates the actual path for the URL named `'home'` (defined back in `reports/urls.py`). Never hardcode `href="/"` — always use `{% url %}`.
- `{% if user.is_authenticated %}` — every template automatically has access to `user` (the logged-in user, or an "anonymous user" object) thanks to the `django.contrib.auth.context_processors.auth` line we added to `TEMPLATES` in Step 5.
- `{% if messages %} ... {{ message.tags }} ...` — this is where every `messages.success(...)` / `messages.info(...)` call from your views actually gets displayed, exactly once, then cleared. `message.tags` becomes `success`, `info`, etc. — matching Bootstrap's `alert-success`, `alert-info` classes automatically.
- Logout is a `<form method="post">`, not a plain link — Django's `LogoutView` only accepts `POST`, so a simple `<a href="/logout/">` wouldn't work (this also protects against accidentally logging someone out just by them visiting a link).

---

## Step 14 — `templates/home.html`

```html
{% extends "base.html" %}
{% block title %}Home | Campus Lost & Found{% endblock %}
{% block content %}

<div class="p-5 mb-4 bg-primary text-white rounded-3">
    <h1 class="display-6 fw-bold">Lost something on campus? Found something?</h1>
    <p class="fs-5">Report it here and help reunite items with their owners.</p>
    {% if user.is_authenticated %}
        <a href="{% url 'report_create' %}" class="btn btn-light btn-lg">+ Create a Report</a>
    {% else %}
        <a href="{% url 'register' %}" class="btn btn-light btn-lg">Get Started</a>
    {% endif %}
</div>

<div class="row mb-4 text-center">
    <div class="col-md-6">
        <div class="card shadow-sm">
            <div class="card-body">
                <h2 class="text-primary">{{ total_active }}</h2>
                <p class="mb-0">Active Reports</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card shadow-sm">
            <div class="card-body">
                <h2 class="text-success">{{ total_resolved }}</h2>
                <p class="mb-0">Resolved Reports</p>
            </div>
        </div>
    </div>
</div>

<h3 class="mb-3">Recent Active Reports</h3>
<div class="row">
    {% for report in recent_reports %}
    <div class="col-md-4 mb-4">
        <div class="card h-100 shadow-sm">
            {% if report.image %}
            <img src="{{ report.image.url }}" class="card-img-top" style="height:180px; object-fit:cover;">
            {% endif %}
            <div class="card-body">
                <span class="badge {% if report.report_type == 'Lost' %}bg-danger{% else %}bg-success{% endif %}">
                    {{ report.report_type }}
                </span>
                <h5 class="card-title mt-2">{{ report.item_name }}</h5>
                <p class="card-text text-muted small">{{ report.category }} &middot; {{ report.location }}</p>
                <a href="{% url 'report_detail' report.pk %}" class="btn btn-outline-primary btn-sm">View Details</a>
            </div>
        </div>
    </div>
    {% empty %}
    <p class="text-muted">No active reports yet.</p>
    {% endfor %}
</div>

<div class="text-center">
    <a href="{% url 'report_list' %}" class="btn btn-secondary">View All Reports</a>
</div>

{% endblock %}
```

`{{ total_active }}` and `recent_reports` come straight from the `context` dictionary the `home` view passed to `render(...)` back in Step 11. `{% for report in recent_reports %} ... {% empty %} ... {% endfor %}` — the `{% empty %}` clause shows only if the list is empty, so you never need a separate `{% if %}` around the loop.

---

## Step 15 — `templates/reports.html` (the searchable list)

```html
{% extends "base.html" %}
{% block title %}All Reports | Campus Lost & Found{% endblock %}
{% block content %}

<h2 class="mb-4">All Lost & Found Reports</h2>

<form method="get" class="row g-2 mb-4 p-3 bg-light rounded border">
    <div class="col-md-4">
        {{ search_form.q.label_tag }}
        {{ search_form.q }}
    </div>
    <div class="col-md-2">
        {{ search_form.report_type.label_tag }}
        {{ search_form.report_type }}
    </div>
    <div class="col-md-2">
        {{ search_form.category.label_tag }}
        {{ search_form.category }}
    </div>
    <div class="col-md-2">
        {{ search_form.status.label_tag }}
        {{ search_form.status }}
    </div>
    <div class="col-md-2 d-flex align-items-end">
        <button type="submit" class="btn btn-primary w-100">Search</button>
    </div>
</form>

<div class="row">
    {% for report in page_obj %}
    <div class="col-md-4 mb-4">
        <div class="card h-100 shadow-sm">
            {% if report.image %}
            <img src="{{ report.image.url }}" class="card-img-top" style="height:180px; object-fit:cover;">
            {% endif %}
            <div class="card-body">
                <span class="badge {% if report.report_type == 'Lost' %}bg-danger{% else %}bg-success{% endif %}">
                    {{ report.report_type }}
                </span>
                <span class="badge {% if report.status == 'Active' %}bg-warning text-dark{% else %}bg-secondary{% endif %}">
                    {{ report.status }}
                </span>
                <h5 class="card-title mt-2">{{ report.item_name }}</h5>
                <p class="card-text text-muted small">{{ report.category }} &middot; {{ report.location }}</p>
                <p class="card-text small">{{ report.description|truncatewords:15 }}</p>
                <a href="{% url 'report_detail' report.pk %}" class="btn btn-outline-primary btn-sm">View Details</a>
            </div>
        </div>
    </div>
    {% empty %}
    <p class="text-muted">No reports match your search.</p>
    {% endfor %}
</div>

{% if page_obj.has_other_pages %}
<nav>
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&{{ request.GET.urlencode }}">Previous</a></li>
        {% endif %}
        <li class="page-item disabled"><span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span></li>
        {% if page_obj.has_next %}
        <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&{{ request.GET.urlencode }}">Next</a></li>
        {% endif %}
    </ul>
</nav>
{% endif %}

{% endblock %}
```

Note: `<form method="get">` here, not `post` — search should be a `GET` request, so the filters show up in the URL (e.g. `?q=ID+Card&report_type=Lost`) and can be bookmarked/shared/refreshed safely. `{{ report.description|truncatewords:15 }}` is a **template filter** — cuts the description down to 15 words for the card preview.

---

## Step 16 — `templates/report_detail.html`

```html
{% extends "base.html" %}
{% block title %}{{ report.item_name }} | Campus Lost & Found{% endblock %}
{% block content %}

<div class="card shadow-sm">
    {% if report.image %}
    <img src="{{ report.image.url }}" class="card-img-top" style="max-height:400px; object-fit:cover;">
    {% endif %}
    <div class="card-body">
        <span class="badge {% if report.report_type == 'Lost' %}bg-danger{% else %}bg-success{% endif %}">
            {{ report.report_type }}
        </span>
        <span class="badge {% if report.status == 'Active' %}bg-warning text-dark{% else %}bg-secondary{% endif %}">
            {{ report.status }}
        </span>

        <h2 class="card-title mt-3">{{ report.item_name }}</h2>
        <p class="text-muted">Category: {{ report.category }}</p>

        <p>{{ report.description }}</p>

        <ul class="list-group list-group-flush mb-3">
            <li class="list-group-item"><strong>Location:</strong> {{ report.location }}</li>
            <li class="list-group-item"><strong>Date:</strong> {{ report.date }}</li>
            <li class="list-group-item"><strong>Contact:</strong> {{ report.contact_info }}</li>
            <li class="list-group-item"><strong>Reported by:</strong> {{ report.owner.username }}</li>
            <li class="list-group-item"><strong>Posted:</strong> {{ report.created_at|date:"M d, Y H:i" }}</li>
        </ul>

        {% if user == report.owner %}
        <div class="d-flex gap-2">
            <a href="{% url 'report_update' report.pk %}" class="btn btn-primary">Edit</a>
            <a href="{% url 'report_delete' report.pk %}" class="btn btn-outline-danger">Delete</a>
            {% if report.status == 'Active' %}
            <form method="post" action="{% url 'report_resolve' report.pk %}">
                {% csrf_token %}
                <input type="hidden" name="next" value="report_detail">
                <button type="submit" class="btn btn-success">Mark as Resolved</button>
            </form>
            {% endif %}
        </div>
        {% endif %}
    </div>
</div>

<a href="{% url 'report_list' %}" class="btn btn-link mt-3">&larr; Back to all reports</a>

{% endblock %}
```

`{% if user == report.owner %}` is what **hides** the Edit/Delete/Resolve buttons from anyone who isn't the owner — but remember, this is just a UI nicety. The *real* security check is the `report.is_owner(request.user)` check inside the views (Step 11) — even if someone crafted a request without seeing this button, the view would still reject them with a 403.

---

## Step 17 — `templates/report_form.html` (shared by both Create and Edit)

```html
{% extends "base.html" %}
{% block title %}{% if is_edit %}Edit Report{% else %}New Report{% endif %} | Campus Lost & Found{% endblock %}
{% block content %}

<h2 class="mb-4">{% if is_edit %}Edit Report{% else %}Create a New Report{% endif %}</h2>

<form method="post" enctype="multipart/form-data" class="card p-4 shadow-sm">
    {% csrf_token %}

    <div class="mb-3">
        <label class="form-label">Item Name</label>
        {{ form.item_name }}
        {{ form.item_name.errors }}
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label class="form-label">Type</label>
            {{ form.report_type }}
            {{ form.report_type.errors }}
        </div>
        <div class="col-md-6 mb-3">
            <label class="form-label">Category</label>
            {{ form.category }}
            {{ form.category.errors }}
        </div>
    </div>

    <div class="mb-3">
        <label class="form-label">Description</label>
        {{ form.description }}
        {{ form.description.errors }}
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label class="form-label">Location</label>
            {{ form.location }}
            {{ form.location.errors }}
        </div>
        <div class="col-md-6 mb-3">
            <label class="form-label">Date</label>
            {{ form.date }}
            {{ form.date.errors }}
        </div>
    </div>

    <div class="mb-3">
        <label class="form-label">Contact Information</label>
        {{ form.contact_info }}
        {{ form.contact_info.errors }}
    </div>

    <div class="mb-3">
        <label class="form-label">Image (optional)</label>
        {% if is_edit and report.image %}
        <div class="mb-2"><img src="{{ report.image.url }}" style="max-height:120px;"></div>
        {% endif %}
        {{ form.image }}
        {{ form.image.errors }}
    </div>

    <button type="submit" class="btn btn-primary">
        {% if is_edit %}Save Changes{% else %}Submit Report{% endif %}
    </button>
    <a href="{% if is_edit %}{% url 'report_detail' report.pk %}{% else %}{% url 'report_list' %}{% endif %}" class="btn btn-secondary">Cancel</a>
</form>

{% endblock %}
```

Two important details:
- **`enctype="multipart/form-data"`** on the `<form>` tag — **required** whenever a form includes a file upload (our optional image). Without it, the image field silently gets dropped and never reaches `request.FILES` in the view.
- **`{% if is_edit %}`** everywhere — this single template serves both `report_create` and `report_update` (Step 11 passed `is_edit=True`/`False` into the context), so the heading, submit button text, and "Cancel" link destination all adapt instead of needing two nearly-identical files.

---

## Step 18 — `templates/report_confirm_delete.html`

```html
{% extends "base.html" %}
{% block title %}Delete Report | Campus Lost & Found{% endblock %}
{% block content %}

<div class="card p-4 shadow-sm">
    <h3>Delete Report</h3>
    <p>Are you sure you want to delete <strong>"{{ report.item_name }}"</strong>? This action cannot be undone.</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Yes, Delete</button>
        <a href="{% url 'report_detail' report.pk %}" class="btn btn-secondary">Cancel</a>
    </form>
</div>

{% endblock %}
```

A deliberately simple confirmation page — `GET` shows this warning; only a real `POST` (the "Yes, Delete" button) triggers `report.delete()` in the view.

---

## Step 19 — `templates/login.html`

```html
{% extends "base.html" %}
{% block title %}Login | Campus Lost & Found{% endblock %}
{% block content %}

<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card p-4 shadow-sm">
            <h3 class="mb-3 text-center">Login</h3>
            <form method="post">
                {% csrf_token %}
                {% for field in form %}
                <div class="mb-3">
                    <label class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="text-danger small">{{ field.errors }}</div>
                    {% endif %}
                </div>
                {% endfor %}
                {% if form.non_field_errors %}
                    <div class="text-danger small mb-2">{{ form.non_field_errors }}</div>
                {% endif %}
                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
            <p class="text-center mt-3 mb-0">
                Don't have an account? <a href="{% url 'register' %}">Register here</a>
            </p>
        </div>
    </div>
</div>

{% endblock %}
```

`{% for field in form %}` — instead of listing `form.username`, `form.password` by hand, this loops over *whatever* fields the form actually has, so it works automatically no matter how the form changes. `form.non_field_errors` catches errors that aren't tied to one specific field — like "wrong username or password."

---

## Step 20 — `templates/register.html`

```html
{% extends "base.html" %}
{% block title %}Register | Campus Lost & Found{% endblock %}
{% block content %}

<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card p-4 shadow-sm">
            <h3 class="mb-3 text-center">Create an Account</h3>
            <form method="post">
                {% csrf_token %}
                {% for field in form %}
                <div class="mb-3">
                    <label class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.help_text %}
                        <div class="form-text">{{ field.help_text }}</div>
                    {% endif %}
                    {% if field.errors %}
                        <div class="text-danger small">{{ field.errors }}</div>
                    {% endif %}
                </div>
                {% endfor %}
                <button type="submit" class="btn btn-primary w-100">Register</button>
            </form>
            <p class="text-center mt-3 mb-0">
                Already have an account? <a href="{% url 'login' %}">Login here</a>
            </p>
        </div>
    </div>
</div>

{% endblock %}
```

Same looping pattern as login, plus `field.help_text` — Django's `UserCreationForm` includes helpful hints (like password requirements) that show up here automatically.

---

## Step 21 — `templates/my_reports.html`

```html
{% extends "base.html" %}
{% block title %}My Reports | Campus Lost & Found{% endblock %}
{% block content %}

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>My Reports</h2>
    <a href="{% url 'report_create' %}" class="btn btn-primary">+ New Report</a>
</div>

{% if page_obj %}
<div class="table-responsive">
<table class="table table-hover align-middle bg-white shadow-sm">
    <thead>
        <tr>
            <th>Item</th>
            <th>Type</th>
            <th>Category</th>
            <th>Status</th>
            <th>Date</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for report in page_obj %}
        <tr>
            <td><a href="{% url 'report_detail' report.pk %}">{{ report.item_name }}</a></td>
            <td>
                <span class="badge {% if report.report_type == 'Lost' %}bg-danger{% else %}bg-success{% endif %}">
                    {{ report.report_type }}
                </span>
            </td>
            <td>{{ report.category }}</td>
            <td>
                <span class="badge {% if report.status == 'Active' %}bg-warning text-dark{% else %}bg-secondary{% endif %}">
                    {{ report.status }}
                </span>
            </td>
            <td>{{ report.date }}</td>
            <td class="d-flex gap-1">
                <a href="{% url 'report_update' report.pk %}" class="btn btn-sm btn-outline-primary">Edit</a>
                <a href="{% url 'report_delete' report.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
                {% if report.status == 'Active' %}
                <form method="post" action="{% url 'report_resolve' report.pk %}">
                    {% csrf_token %}
                    <input type="hidden" name="next" value="my_reports">
                    <button type="submit" class="btn btn-sm btn-outline-success">Resolve</button>
                </form>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
</div>

{% if page_obj.has_other_pages %}
<nav>
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a></li>
        {% endif %}
        <li class="page-item disabled"><span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span></li>
        {% if page_obj.has_next %}
        <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a></li>
        {% endif %}
    </ul>
</nav>
{% endif %}

{% else %}
<p class="text-muted">You haven't created any reports yet.</p>
{% endif %}

{% endblock %}
```

Same data (`page_obj`) as `reports.html`, but pre-filtered by the view to just the logged-in user's own reports (Step 11, `my_reports` view) — no ownership check needed here since the query already guarantees it.

---

## Step 22 — `static/css/style.css`

```css
body {
    background-color: #f5f6fa;
}

/* Ensure any Django-rendered inputs (e.g. built-in auth forms) match Bootstrap styling */
input[type="text"],
input[type="password"],
input[type="email"],
input[type="date"],
input[type="file"],
select,
textarea {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    border: 1px solid #ced4da;
    border-radius: 0.375rem;
    background-color: #fff;
}

.card-title {
    font-weight: 600;
}
```

**Why this file exists:** Django's built-in login form doesn't know about Bootstrap CSS classes, so instead of hand-editing every input's `class` attribute, this stylesheet styles raw `<input>`/`<select>`/`<textarea>` tags directly — a shortcut so *every* form looks consistent with almost no extra template work.

---

## Step 23 — Run it for real

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Walk through this checklist in order:

1. **Register** at `/register/` → you should land back on the home page, logged in, with a green "Welcome" message.
2. **Create a report** via "+ New Report" → fill every field, try uploading an image → you land on the detail page with "Report created successfully!"
3. **Browse** `/reports/` → your report appears as a card. Try the search box and the Type/Category/Status dropdowns.
4. **Edit** it from "My Reports" → change something → "Report updated successfully!"
5. **Resolve** it → status badge flips to "Resolved," button disappears (since the template only shows Resolve while `status == 'Active'`).
6. **Log out**, register a **second** account, and try visiting `/reports/1/edit/` directly in the address bar — you should get a plain "403 Forbidden" page. That confirms the ownership check in the view is doing its job, independent of the UI.
7. **Delete** the report from your first account → confirmation page → "Report deleted successfully!"
8. Watch your terminal the whole time — every single request prints a line such as:
   ```
   User: rahim | Method: POST | Path: /reports/create/ | Time: 0.02s
   ```
9. Visit `/admin/`, log in with the superuser you created in Step 8, and browse the `Report` table — try the search box and filters there too.

If every one of those 9 steps behaved as described, you've built — and correctly verified — the entire system yourself, from an empty folder to a working multi-user CRUD app with authentication, search, permissions, custom middleware, and messages.

---

## Final file tree (what you should have now)

```
campus_lostfound/
├── manage.py
├── requirements.txt
├── db.sqlite3                    (created by migrate)
├── campus_lostfound/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── reports/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── reports.html
│   ├── report_detail.html
│   ├── report_form.html
│   ├── report_confirm_delete.html
│   ├── login.html
│   ├── register.html
│   └── my_reports.html
└── static/
    └── css/
        └── style.css
```

If anything doesn't run, re-check these two things first, in this order — they cause 90% of beginner errors: (1) is `venv` activated (do you see `(venv)` in your prompt)? (2) did you run `makemigrations` *then* `migrate` after the last time you touched `models.py`?
