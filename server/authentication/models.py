from server.authentication.managers import CallBackTokenManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import generate_numeric_token
from django.conf import settings


class CallbackToken(models.Model):
    TOKEN_TYPE_AUTH = 'AUTH'
    TOKEN_TYPE_VERIFY = 'VERIFY'
    TOKEN_PASSWORD_RESET = 'PASSWORD_RESET'
    TOKEN_TYPES = (
        (TOKEN_TYPE_AUTH, 'Autenticación'),
        (TOKEN_TYPE_VERIFY , 'Verificación'),
        (TOKEN_PASSWORD_RESET, 'Reestablecer contraseña'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="USUARIO")
    key = models.CharField(default=generate_numeric_token, max_length=6, verbose_name="CÓDIGO ENVIADO")
    type = models.CharField(choices=TOKEN_TYPES, max_length=30, verbose_name="TIPO")
    to_alias = models.CharField(blank=True, null=True, max_length=30, verbose_name="TIPO ALIAS")
    to_alias_type = models.CharField(blank=True, null=True, max_length=30, verbose_name="PARA ALIAS TIPO")
    ip_address = models.GenericIPAddressField(blank=True, null=True, default='', verbose_name="DIRECCIÓN IP DE LA PETICIÓN")
    user_agent = models.CharField(max_length=256, verbose_name="DISPOSITIVO DE PETICIÓN", default="", blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="ACTIVO")

    created_at = models.DateTimeField(auto_now=True, verbose_name="CREADO")

    objects = CallBackTokenManager()

    class Meta:
        app_label = 'authentication'
        ordering = ['-created_at']
        verbose_name = _('Tokens')
        verbose_name_plural = _('Tokens')

    def __str__(self):
        return self.key
