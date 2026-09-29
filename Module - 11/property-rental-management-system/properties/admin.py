from django.contrib import admin
from .models import Property
# addition of image gallery for a property
from .models import PropertyImage

# addition of image gallery for a property
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'location',
                     'monthly_rent', 'is_available', 'created_at')
    list_filter = ('property_type', 'is_available', 'created_at')
    search_fields = ('title', 'location', 'owner__username')
    list_editable = ('is_available',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    # addition of image gallery for a property
    inlines = [PropertyImageInline]
