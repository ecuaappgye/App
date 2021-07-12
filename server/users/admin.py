from django.contrib import admin
from .models import BaseUser

class BaseUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("full_name", "email", "created_at")
    search_fields = ("email",)

admin.site.register(BaseUser, BaseUserAdmin)