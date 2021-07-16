from django.contrib import admin
from .models import BaseUser, Rol, Document
from django.contrib.sessions.models import Session

class BaseUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("full_name", "email", "rol_name", "created_at")
    search_fields = ("email",)
    list_filter = ['created_at']

admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(Session)


class RolAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("name", "created_at")
    search_fields = ("name",)
admin.site.register(Rol, RolAdmin)

class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
admin.site.register(Document, DocumentAdmin)
