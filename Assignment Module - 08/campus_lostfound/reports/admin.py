from django.contrib import admin
from .models import Report

# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'report_type', 'category', 'status', 'owner', 'date', 'created_at')
    list_filter = ('report_type', 'category', 'status')
    search_fields = ('item_name', 'description', 'location')