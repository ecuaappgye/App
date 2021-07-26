import string

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


def generate_numeric_token():
    # Genera un cadena string con una longitud máxima de 6 dígitos.
    return get_random_string(length=6, allowed_chars=string.digits)


class CallbackToken(models.Model):
    TOKEN_TYPE_AUTH = 'AUTH'
    TOKEN_TYPE_VERIFY = 'VERIFY'
    TOKEN_TYPES = ((TOKEN_TYPE_AUTH, 'Auth'), (TOKEN_TYPE_VERIFY, 'Verify'))

    user = models.ForeignKey(
        'users.BaseUser', on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(default=generate_numeric_token, max_length=6)
    type = models.CharField(choices=TOKEN_TYPES, max_length=20)
    to_alias = models.CharField(blank=True, null=True, max_length=20)
    to_alias_type = models.CharField(blank=True, null=True, max_length=20)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'authentication'
        ordering = ['-created_at']
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def __str__(self):
        return self.key
