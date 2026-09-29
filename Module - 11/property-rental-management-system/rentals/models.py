from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RentalRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE, related_name='rental_requests'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_requests'
    )
    message = models.TextField(blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.tenant} -> {self.property} [{self.status}]"


class Review(models.Model):
    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE, related_name='reviews'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'tenant')

    def __str__(self):
        return f"{self.tenant} rated {self.property} - {self.rating}/5"
