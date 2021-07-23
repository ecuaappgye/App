from django.db import models
from django.utils import timezone
from .services import generate_numeric_token


class CallbackToken(models.Model):
    TOKEN_TYPE_AUTH = 'AUTH'
    TOKEN_TYPE_VERIFY = 'VERIFY'
    TOKEN_TYPES = ((TOKEN_TYPE_AUTH, 'Auth'), (TOKEN_TYPE_VERIFY, 'Verify'))

    user = models.ForeignKey('users.BaseUser', on_delete=models.CASCADE)
    key = models.CharField(default=generate_numeric_token, max_length=6)
    type = models.CharField(choices=TOKEN_TYPES, max_length=20)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
