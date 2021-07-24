from django.core.exceptions import ValidationError
from .models import CallbackToken


def callbacktoken_by_user(*, id:int):
    try:
        return CallbackToken.objects.get(id=id, is_active=True)
    except CallbackToken.DoesNotExist :
        raise ValidationError('Usuario no encontrado.')

