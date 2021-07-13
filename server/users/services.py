from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from server.users.selectors import user_by_email, user_by_id
from django.utils.encoding import smart_bytes
from .models import BaseUser


def user_create(*,
    first_name:str,
    last_name:str, 
    email:str, 
    password:str,
    id_rol:str,
    avatar
    )->BaseUser:
    
    user = BaseUser.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        avatar=avatar
    )

    # Add role user
    user.rol_id = id_rol
    user.save()

    return user


def user_update_profile(*, user_id:int, data)->BaseUser:

    user = user_by_id(id=user_id)

    return user


def user_password_reset(*, email:str)->BaseUser:
   user = user_by_email(email=email)

   token = user_make_token(user_id=user.id)

   # Avanzar la concatenación url

   return user


def user_make_token(*, user_id:int):
    user = urlsafe_base64_encode(smart_bytes(user_id))

    return user
