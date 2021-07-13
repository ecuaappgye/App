from django.core.exceptions import ValidationError
from .models import BaseUser


def user_data(*, user)->BaseUser:
    return {
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "address":user.address,
        "rol_name":user.rol_name,
        "is_driver":user.is_driver,
        "is_client":user.is_client
    }

def user_by_id(*, id:int)->BaseUser:
    try:
        return BaseUser.objects.get(id=id)
    except BaseUser.DoesNotExist:
        raise ValidationError("Usuario no encontrado.")
    
def user_by_email(*, email:str):
    try:
        return BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        raise ValidationError("Usuario no encontrado.")