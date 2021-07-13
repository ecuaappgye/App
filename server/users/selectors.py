from django.core.exceptions import ValidationError
from .models import BaseUser


def user_data(*, user)->BaseUser:
    return {
        "first_name":user.first_name
    }


def user_by_id(*, id:int)->BaseUser:
    try:
        return BaseUser.objects.get(id=id)
    except BaseUser.DoesNotExist:
        raise ValidationError("Usuario no encontrado.")        