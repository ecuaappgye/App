from django.contrib import admin
from .models import BaseUser, DocumentTypeRol, Rol, DocumentType, UserDocumentTypeRol
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _


class BaseUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("full_name", "email", "created_at")
    search_fields = ("email",)
    list_filter = ['created_at']
admin.site.register(BaseUser, BaseUserAdmin)

class SessionAdmin(admin.ModelAdmin):
    def user_session(self, object):
        session_decode = object.get_decoded()
        user_id = session_decode.get('_auth_user_id')
        return BaseUser.objects.get(id=user_id)
    list_display = ('user_session', 'expire_date' )
admin.site.register(Session, SessionAdmin)

class RolAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("name", "created_at")
    search_fields = ("name",)
admin.site.register(Rol, RolAdmin)

class DocumentTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("name", "description")
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(DocumentTypeRol)
admin.site.register(UserDocumentTypeRol)

