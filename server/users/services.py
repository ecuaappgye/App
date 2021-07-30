from datetime import datetime
from threading import Thread

from config.settings.env_reader import env
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from server.authentication.models import CallbackToken
from server.authentication.selectors import (callback_token_by_token,
                                             callback_token_by_user_id)
from server.authentication.services import (create_token_callback_for_user,
                                            invalidate_previous_tokens)
from server.authentication.utils import validate_token
from server.users.selectors import user_by_email, user_by_id

from .models import BaseUser
from .utils import (send_email_email_change, send_email_password_change,
                    send_email_password_reset_check_for_user,
                    send_email_password_reset_for_user, validate_password)


def user_create(*,first_name: str,
                last_name: str,
                email: str,
                password: str,
                avatar,
                is_active: bool=False
                ) -> BaseUser:

    user = BaseUser.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        avatar=avatar,
        is_active=is_active)

    return user


def user_update_profile(*, user_id: int, data) -> BaseUser:
    """Servicio que permite actualizar los datos de perfil del usuario.
    Los campos declarados en el array de 'valid_fields' son únicamente
    permitidos por no ser considerados sensibles.

    Parámetros:
    user_id -> Identificación del usuario
    data -> Información de actualización
    """
    user = user_by_id(id=user_id)

    if not data:
        raise ValidationError(settings.USER_REQUIRED_FIELDS)

    valid_fields = [
        'first_name',
        'last_name',
        'address',
        'avatar',
        'cdi',
        'phone'
    ]

    update_fields = []
    # Chequear si se ha enviado una imagen en la data.
    # Procesar la imagen
    avatar = data.get("avatar")
    if avatar:
        pass

    for field in valid_fields:
        if field in data:
            setattr(user, field, data[field])
            update_fields.append(field)

    if not update_fields:
        return None

    user.save(update_fields=update_fields)

    return user


def user_password_reset(*, email: str, ip_address:str, user_agent:str ) -> CallbackToken:
    """Servicio que permite enviar un correo electrónico con
    un token para el reestablecimiento de contraseña. En en caso
    de que el correo no sea válido se enviara un error.

    Parámetros:
    email -> Correo electrónico del usuario.
    ip_address -> Dirección ip de la máquina de petición.
    user_agent -> Usuario agente de petición.
    """
    user = user_by_email(email=email)

    callback_token_data = {
        'user_id': user.id, 
        'alias_type': 'email',
        'token_type': CallbackToken.TOKEN_PASSWORD_RESET,
        'ip_address': ip_address,
        'user_agent': user_agent
    }

    token = create_token_callback_for_user(data = callback_token_data)
    invalidate_previous_tokens(callback_token=token)

    return token


def user_password_reset_check(*, token: str, new_password: str, password_confirm: str):
    """Servicio que permite revisar el token y la nueva contraseña para poder
    actualizar su nueva contraseña.

    Parámetros:
    token -> Código de verificación
    ip_address -> Nueva contraseña
    user_agent -> Nueva contraseña confirmación
    new_password ->
    password_confirm ->
    """
    if new_password != password_confirm:
        raise ValidationError(settings.USER_PASSWORD_NO_MATCH)

    token_user = callback_token_by_token(token=token)
    validate_token(token=token, token_compare=token_user.key)

    user = user_by_id(id=token_user.user.id)
    validate_password(password=new_password, user=user)
    user.set_password(new_password)
    user.save(update_fields=["password"])

    return user


def user_password_change(*, user_id: int, old_password: str, new_password: str, password_confirm):
    user = user_by_id(id=user_id)

    if new_password != password_confirm:
        raise ValidationError("Contraseñas no coinciden.")

    # Validar si la contraseña enviada es válida
    if not user.check_password(old_password):
        raise ValidationError("Contraseña anterior no es válida.")

    validate_password(password=new_password, user=user)
    user.set_password(new_password)
    user.save(update_fields=["password"])

    # Envío de notificación en un nuevo proceso.
    Thread(target=send_email_password_change,
           args=(user, None)).start()

    return user


def user_email_change(*, user_id, email):
    """Servicio que permite cambiar de cuenta de correo electrónico.

    Parámetros:
    user_id -> Identificación del usuario
    email -> Nuevo correo electrónico
    """
    user = user_by_id(id=user_id)
    user.email = email
    user.save(update_fields=["email"])

    # Notificar en un nuevo proceso del sistema operativo
    # Thread(target=send_email_email_change,
    #     args=(user, None)).start()

    return user

# =============
# Sessions
# =============

def user_unique_session(*, user: BaseUser):
    """Eliminar sesión si ya existe el usuario.
    Borrar la sesión del usuario actual de la base de datos.
    Denegar el acceso al usuario.
    """
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    if not sessions:
        return None

    for session in sessions:
        session_decode = session.get_decoded()
        if '_auth_user_id' in session_decode:
            if user.id == int(session_decode.get('_auth_user_id')):
                session.delete()
                return True


def user_account_active(*, credentials:str):
    """Función que permite determinar si la cuenta de un usuario 
    está activa.
    """
    try:
        if not BaseUser.objects.get(email=credentials.get('email')).is_active:
            raise ValidationError(settings.USER_ACCOUNT_INACTIVE)
        
    except BaseUser.DoesNotExist:
        return None
