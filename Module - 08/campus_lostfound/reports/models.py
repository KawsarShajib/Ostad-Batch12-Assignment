## Step 6 — Define the database model

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Report(models.Model):
    TYPE_LOST = 'Lost'
    TYPE_FOUND = 'Found'
    TYPE_CHOICES = [
        (TYPE_LOST, 'Lost'),
        (TYPE_FOUND, 'Found'),
    ]

    CATEGORY_CHOICES = [
        ('Documents', 'Documents'),
        ('Electronics', 'Electronics'),
        ('Accessories', 'Accessories'),
        ('Clothing', 'Clothing'),
        ('Keys', 'Keys'),
        ('Bags', 'Bags'),
        ('Others', 'Others'),
    ]

    STATUS_ACTIVE = 'Active'
    STATUS_RESOLVED = 'Resolved'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    item_name = models.CharField(max_length=150)
    report_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField(help_text="Date the item was lost or found")
    contact_info = models.CharField(max_length=150, help_text="Phone number or email")
    image = models.ImageField(upload_to='report_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.report_type}] {self.item_name} ({self.status})"

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})

    def is_owner(self, user):
        return self.owner_id == user.id


## Step 6 — Define the database model

"""
**What's happening here, field by field:**
---------------------------------------------

owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports') :
— this is the single most important line in the whole project. It creates a link from every `Report` row to exactly one `User` row. `on_delete=models.CASCADE` means "if that user is deleted, delete their reports too." 

related_name='reports' :
- means you could later write `some_user.reports.all()` to get all of someone's reports.

CharField vs TextField :
`CharField` needs a `max_length` and is meant for short text (names, locations). 
`TextField` has no length limit and is for long free text (the description).

choices=TYPE_CHOICES : 
— restricts the field to a fixed list of options. Each entry is a `(stored_value, human_readable_label)` pair. Django auto-renders these as a dropdown (`<select>`) in forms.

ImageField(upload_to='report_images/', blank=True, null=True) :
— an optional photo. `blank=True` = optional in forms; `null=True` = the database column is allowed to be empty. `upload_to` says where inside `MEDIA_ROOT` uploaded files get saved.

auto_now_add=True` vs `auto_now=True :
— the first sets the timestamp once, when the row is first created (`created_at`); the second updates it every single time the row is saved (`updated_at`).

class Meta: ordering = ['-created_at']
— newest reports show up first by default, everywhere, without any view needing to say so.

is_owner(self, user) : 
— a small helper method we wrote by hand. We'll call `report.is_owner(request.user)` constantly in views to check permissions, instead of repeating `report.owner_id == request.user.id` everywhere.

"""