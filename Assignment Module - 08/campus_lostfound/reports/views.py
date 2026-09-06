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