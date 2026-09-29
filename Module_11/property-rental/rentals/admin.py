from django.contrib import admin
from .models import RentalRequest, Review


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'tenant', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('property__title', 'tenant__username')
    list_editable = ('status',)
    date_hierarchy = 'request_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('property__title', 'tenant__username', 'comment')
