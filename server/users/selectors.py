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
        "phone": user.phone
    }

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


def user_model_fields(*, user_data):
    # Actulizar el array de envío de data 
    # Si cambian atributos de creación de conductor.
    if not user_data:
        raise ValidationError('Usuario no contiene atributos.')

    data = []
    valid_fields = [e for e in user_data]
    
    output = { 'CharField':'text',
               'FileField':'file',
               'TextField':'textarea',
               'EmailField':'email'}
    

    for field in BaseUser._meta.fields:
        if field.attname in valid_fields:
            data.append({
                'name': field.verbose_name,
                'length': field.max_length,
                'null': field.null,
                'type': output.get(field.get_internal_type())
            })

    return data
