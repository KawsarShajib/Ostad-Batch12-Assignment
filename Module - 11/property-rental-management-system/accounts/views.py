from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterForm, ProfileUpdateForm
from properties.models import Property
from rentals.models import RentalRequest


def register_view(request):
    if request.user.is_authenticated:
        return redirect('properties:list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect('properties:list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'properties:list'


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    """Redirect to the correct dashboard based on role."""
    if request.user.is_owner:
        properties = Property.objects.filter(owner=request.user)
        requests_qs = RentalRequest.objects.filter(property__owner=request.user)
        context = {
            'total_properties': properties.count(),
            'available_properties': properties.filter(is_available=True).count(),
            'total_requests': requests_qs.count(),
            'pending_requests': requests_qs.filter(status='PENDING').count(),
            'accepted_requests': requests_qs.filter(status='ACCEPTED').count(),
            'properties': properties.order_by('-created_at')[:5],
            'recent_requests': requests_qs.order_by('-request_date')[:5],
        }
        return render(request, 'accounts/owner_dashboard.html', context)
    else:
        requests_qs = RentalRequest.objects.filter(tenant=request.user)
        context = {
            'total_requests': requests_qs.count(),
            'pending_requests': requests_qs.filter(status='PENDING').count(),
            'accepted_requests': requests_qs.filter(status='ACCEPTED').count(),
            'rejected_requests': requests_qs.filter(status='REJECTED').count(),
            'recent_requests': requests_qs.order_by('-request_date')[:5],
        }
        return render(request, 'accounts/tenant_dashboard.html', context)
