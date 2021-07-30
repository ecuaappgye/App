from typing import ClassVar

from django.conf import settings
from .models import CallbackToken
from django.core.exceptions import ValidationError


def callback_token_by_user_id(*, id: int) -> CallbackToken:
    try:
        return CallbackToken.objects.get(user_id=id, is_active=True)
    except CallbackToken.DoesNotExist:
        raise ValidationError('Usuario no tiene aliado un token.')


def callback_token_by_token(*, token:str) -> CallbackToken:
    try:
        return CallbackToken.objects.get(key=token, is_active=True)
    except CallbackToken.DoesNotExist:
        raise ValidationError(settings.VERIFY_TOKEN_FAILED_MESSAGE)