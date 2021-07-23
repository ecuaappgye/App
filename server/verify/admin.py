from django.contrib import admin
from .models import CallbackToken


class CallbackTokenAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("user", "key", "created_at")
    search_fields = ("user",)
    list_filter = ['created_at']

admin.site.register(CallbackToken, CallbackTokenAdmin)