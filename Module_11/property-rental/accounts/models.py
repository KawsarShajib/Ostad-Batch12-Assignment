from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a role: property owner or tenant."""

    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Property Owner'
        TENANT = 'TENANT', 'Tenant'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TENANT)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_tenant(self):
        return self.role == self.Role.TENANT
