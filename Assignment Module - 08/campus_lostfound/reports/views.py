from django.shortcuts import render
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
# Create your views here.


def home(request):
    """Landing page: shows a few recent active reports and quick stats."""
    recent_reports = Report.objects.filter(status=Report.STATUS_ACTIVE)[:6]
    context = {
        'recent_reports': recent_reports,
        'total_active': int(Report.objects.filter(status=Report.STATUS_ACTIVE).count()),
        'total_resolved': int(Report.objects.filter(status=Report.STATUS_RESOLVED).count()),
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




## Step 11 — Write `reports/views.py`

# Replace the contents of the auto-generated `reports/views.py`:

"""

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


"""
