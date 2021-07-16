from django.contrib import admin
from .models import Retention

class RetentionAdmin (admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("service_total", "service_supervisor", "service_app", "created_at")
    list_filter = ['created_at']
admin.site.register (Retention, RetentionAdmin) 
