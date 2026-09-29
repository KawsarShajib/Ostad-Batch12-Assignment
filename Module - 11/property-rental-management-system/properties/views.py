from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PropertyForm, PropertySearchForm
from .models import Property
from rentals.forms import RentalRequestForm, ReviewForm
from rentals.models import RentalRequest, Review

# addition of image gallery for a property
# ----------------------------------------
from .forms import PropertyForm, PropertyImageFormSet
from .models import Property, PropertyImage



def property_list(request):
    properties = Property.objects.filter(is_available=True).select_related('owner')
    form = PropertySearchForm(request.GET or None)

    if form.is_valid():
        location = form.cleaned_data.get('location')
        property_type = form.cleaned_data.get('property_type')
        min_rent = form.cleaned_data.get('min_rent')
        max_rent = form.cleaned_data.get('max_rent')

        if location:
            properties = properties.filter(location__icontains=location)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if min_rent is not None:
            properties = properties.filter(monthly_rent__gte=min_rent)
        if max_rent is not None:
            properties = properties.filter(monthly_rent__lte=max_rent)

    paginator = Paginator(properties, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'properties/property_list.html', {
        'page_obj': page_obj,
        'form': form,
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    reviews = property_obj.reviews.select_related('tenant').order_by('-created_at')

    can_request = False
    existing_pending_request = None
    can_review = False
    review_form = None
    request_form = None

    if request.user.is_authenticated and request.user.is_tenant:
        request_form = RentalRequestForm()
        existing_pending_request = RentalRequest.objects.filter(
            property=property_obj, tenant=request.user, status='PENDING'
        ).first()
        can_request = (
            property_obj.is_available
            and property_obj.owner_id != request.user.id
            and existing_pending_request is None
        )

        has_accepted_request = RentalRequest.objects.filter(
            property=property_obj, tenant=request.user, status='ACCEPTED'
        ).exists()
        already_reviewed = Review.objects.filter(
            property=property_obj, tenant=request.user
        ).exists()
        can_review = has_accepted_request and not already_reviewed
        if can_review:
            review_form = ReviewForm()

    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'reviews': reviews,
        'can_request': can_request,
        'request_form': request_form,
        'can_review': can_review,
        'review_form': review_form,
    })


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()

            # addition of image gallery for a property
            formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
            if formset.is_valid():
                formset.save()

            messages.success(request, "Property listed successfully.")
            return redirect('properties:detail', pk=property_obj.pk)
        # addition of image gallery for a property
        formset = PropertyImageFormSet(request.POST, request.FILES)
    else:
        form = PropertyForm()
        # addition of image gallery for a property
        formset = PropertyImageFormSet()
    return render(request, 'properties/property_form.html', {'form': form, 'formset': formset, 'action': 'Add'})


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.owner_id != request.user.id:
        messages.error(request, "You may only edit your own properties.")
        return redirect('properties:detail', pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        # addition of image gallery for a property
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Property updated successfully.")
            return redirect('properties:detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
        # addition of image gallery for a property
        formset = PropertyImageFormSet(instance=property_obj)
    return render(request, 'properties/property_form.html', {'form': form, 'formset': formset, 'action': 'Edit'})


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.owner_id != request.user.id:
        messages.error(request, "You may only delete your own properties.")
        return redirect('properties:detail', pk=pk)

    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Property deleted.")
        return redirect('accounts:dashboard')
    return render(request, 'properties/property_confirm_delete.html', {'property': property_obj})


# addition of image gallery for a property
@login_required
def delete_property_image(request, pk):
    """Quick single-image removal straight from the property detail page,
    without going through the full edit form."""
    image = get_object_or_404(PropertyImage, pk=pk)
    if image.property.owner_id != request.user.id:
        messages.error(request, "You may only manage images on your own properties.")
        return redirect('properties:detail', pk=image.property_id)

    property_pk = image.property_id
    if request.method == 'POST':
        image.delete()
        messages.success(request, "Image removed.")
    return redirect('properties:detail', pk=property_pk)


@login_required
def my_properties(request):
    if not request.user.is_owner:
        messages.error(request, "Only property owners have a property list.")
        return redirect('properties:list')
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/my_properties.html', {'properties': properties})




