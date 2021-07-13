from django.contrib import admin
from .models import BaseUser, Rol, Document

class BaseUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("full_name", "email", "created_at")
    search_fields = ("email",)
admin.site.register(BaseUser, BaseUserAdmin)

class RolAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("name", "created_at")
    search_fields = ("name",)
admin.site.register(Rol, RolAdmin)

class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
admin.site.register(Document, DocumentAdmin)
