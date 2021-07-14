from django.contrib import admin
from .models import Email

class EmailAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_sent'
    list_display = ("user", "subject", "date_sent")
    list_filter = ['date_sent']
admin.site.register(Email, EmailAdmin)