## Step 8 — Register the model with Django admin

from django.contrib import admin
from .models import Report

# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'report_type', 'category', 'status', 'owner', 'date', 'created_at')
    list_filter = ('report_type', 'category', 'status')
    search_fields = ('item_name', 'description', 'location')




## Step 8 — Register the model with Django admin

"""
Why : 
------
this one small file unlocks a full admin dashboard at `/admin/` — a searchable, filterable table of every report, with built-in edit/delete — without you writing a single view or template for it.
 
`list_display` controls the columns shown; 
`list_filter` adds sidebar filters; 
`search_fields` adds a search box.

Also confirm `reports/apps.py` looks like this (Django generated it, no changes needed, shown for completeness):

```python
from django.apps import AppConfig

class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
```

"""