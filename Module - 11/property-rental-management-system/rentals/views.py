from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RentalRequestForm, ReviewForm
from .models import RentalRequest, Review
from .emails import send_new_request_email, send_request_status_email, send_request_cancelled_email
from properties.models import Property


@login_required
def send_request(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    if not request.user.is_tenant:
        messages.error(request, "Only tenants can send rental requests.")
        return redirect('properties:detail', pk=property_id)

    if property_obj.owner_id == request.user.id:
        messages.error(request, "You cannot request your own property.")
        return redirect('properties:detail', pk=property_id)

    if not property_obj.is_available:
        messages.error(request, "This property is not currently available.")
        return redirect('properties:detail', pk=property_id)

    already_pending = RentalRequest.objects.filter(
        property=property_obj, tenant=request.user, status=RentalRequest.Status.PENDING
    ).exists()
    if already_pending:
        messages.warning(request, "You already have a pending request for this property.")
        return redirect('properties:detail', pk=property_id)

    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_request = form.save(commit=False)
            rental_request.property = property_obj
            rental_request.tenant = request.user
            rental_request.save()
            send_new_request_email(rental_request)
            messages.success(request, "Your rental request has been sent.")
            return redirect('rentals:my_requests')
    else:
        form = RentalRequestForm()

    return render(request, 'rentals/request_form.html', {'form': form, 'property': property_obj})


@login_required
def my_requests(request):
    if not request.user.is_tenant:
        messages.error(request, "Only tenants have rental requests to view.")
        return redirect('properties:list')
    requests_qs = RentalRequest.objects.filter(tenant=request.user).select_related('property')
    return render(request, 'rentals/my_requests.html', {'requests': requests_qs})


@login_required
def cancel_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk)

    if rental_request.tenant_id != request.user.id:
        messages.error(request, "You may only cancel your own requests.")
        return redirect('rentals:my_requests')

    if rental_request.status != RentalRequest.Status.PENDING:
        messages.error(request, "Only pending requests can be cancelled.")
        return redirect('rentals:my_requests')

    if request.method == 'POST':
        rental_request.status = RentalRequest.Status.CANCELLED
        rental_request.save()
        send_request_cancelled_email(rental_request)
        messages.success(request, "Request cancelled.")
        return redirect('rentals:my_requests')

    return render(request, 'rentals/request_confirm_cancel.html', {'rental_request': rental_request})


@login_required
def owner_requests(request):
    if not request.user.is_owner:
        messages.error(request, "Only property owners can view received requests.")
        return redirect('properties:list')
    requests_qs = RentalRequest.objects.filter(
        property__owner=request.user
    ).select_related('property', 'tenant')
    return render(request, 'rentals/owner_requests.html', {'requests': requests_qs})


@login_required
def accept_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk)

    if rental_request.property.owner_id != request.user.id:
        messages.error(request, "You can only manage requests for your own properties.")
        return redirect('rentals:owner_requests')

    if rental_request.status != RentalRequest.Status.PENDING:
        messages.error(request, "Only pending requests can be accepted.")
        return redirect('rentals:owner_requests')

    rental_request.status = RentalRequest.Status.ACCEPTED
    rental_request.save()
    send_request_status_email(rental_request)
    messages.success(request, f"Request from {rental_request.tenant.username} accepted.")
    return redirect('rentals:owner_requests')


@login_required
def reject_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk)

    if rental_request.property.owner_id != request.user.id:
        messages.error(request, "You can only manage requests for your own properties.")
        return redirect('rentals:owner_requests')

    if rental_request.status != RentalRequest.Status.PENDING:
        messages.error(request, "Only pending requests can be rejected.")
        return redirect('rentals:owner_requests')

    rental_request.status = RentalRequest.Status.REJECTED
    rental_request.save()
    send_request_status_email(rental_request)
    messages.success(request, f"Request from {rental_request.tenant.username} rejected.")
    return redirect('rentals:owner_requests')


@login_required
def add_review(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    if not request.user.is_tenant:
        messages.error(request, "Only tenants can leave reviews.")
        return redirect('properties:detail', pk=property_id)

    has_accepted_request = RentalRequest.objects.filter(
        property=property_obj, tenant=request.user, status=RentalRequest.Status.ACCEPTED
    ).exists()
    if not has_accepted_request:
        messages.error(request, "You can only review properties after an accepted rental request.")
        return redirect('properties:detail', pk=property_id)

    if Review.objects.filter(property=property_obj, tenant=request.user).exists():
        messages.warning(request, "You have already reviewed this property.")
        return redirect('properties:detail', pk=property_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property_obj
            review.tenant = request.user
            review.save()
            messages.success(request, "Thanks for leaving a review!")
    return redirect('properties:detail', pk=property_id)