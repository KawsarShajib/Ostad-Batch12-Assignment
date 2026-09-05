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