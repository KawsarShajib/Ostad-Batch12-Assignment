from django.conf import settings
from django.db import models
from django.urls import reverse


class Property(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = 'APARTMENT', 'Apartment'
        HOUSE = 'HOUSE', 'House'
        ROOM = 'ROOM', 'Room'
        OFFICE = 'OFFICE', 'Office'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    location = models.CharField(max_length=255)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()}) - {self.location}"

    def get_absolute_url(self):
        return reverse('properties:detail', args=[self.pk])

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)


# addition of image gallery for a property
# ----------------------------------------
class PropertyImage(models.Model):
    """Extra gallery photos for a property. `Property.image` stays the
    single cover photo used on listing cards; these show on the detail page."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='gallery_images'
    )
    image = models.ImageField(upload_to='property_gallery/')
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.property.title}"
