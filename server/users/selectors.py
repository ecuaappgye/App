from django.core.exceptions import ValidationError
from .models import BaseUser


def user_data(*, user)->BaseUser:
    try:
        return {
        'id': user.id, 
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "avatar": user.avatar.url if user.avatar else None,
        "cdi": user.cdi,
        "phone": user.phone}

    except Exception :
        raise ValidationError("Usuario no encontrado.")

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

def user_by_id_data(*, id:int):
    user = user_by_id(id=id)
    
    return user_data(user=user)