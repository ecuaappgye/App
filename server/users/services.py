from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from server.users.selectors import user_by_email, user_by_id
from config.settings.env_reader import env

from .models import BaseUser
from .utils import send_email_password_reset_for_user, validate_password


def user_create(*,
    first_name:str,
    last_name:str, 
    email:str, 
    password:str,
    avatar
    )->BaseUser:
    
    user = BaseUser.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        avatar=avatar
    )
    
    return user


def user_update_profile(*, user_id:int, data)->BaseUser:
    """Servicio que permite actualizar los datos de perfil del usuario.
    Los campos declarados en el array de 'valid_fields' son únicamente
    permitidos por no ser considerados sensibles.

    Parámetros:
    user_id -> Identificación del usuario
    data -> Información de actualización
    """
    user = user_by_id(id=user_id)

    valid_fields =[
        "first_name",
        "last_name",
        "address",
        "avatar"
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

    user.save(update_fields=update_fields)

    return user


def user_password_reset(*, email:str)->BaseUser:
    """Servicio que permite enviar un correo electrónico con
    un token para el reestablecimiento de contraseña. En en caso
    de que el correo no sea válido se enviara un error.

    Parámetros:
    email -> Correo electrónico del usuario.
    """
    token = user_make_token(email=email)
    user = user_by_email(email=email)
    # Envio de correo electrónico utilizando el usuario.
    # Envío de token en el contexto del parámetro
    extra_context = {"token": token}
    send_email_password_reset_for_user(user=user, extra_context=extra_context)

    return token


def user_password_reset_check(*, token:str, new_password:str, password_confirm:str):
    """Servicio que permite revisar el token y la nueva contraseña para poder
    actualizar su nueva contraseña.
    
    Parámetros:
    token -> Código de verificación
    new_password -> Nueva contraseña
    password_confirm -> Nueva contraseña confirmación
    """
    token_user = user_extract_token(token=token)
    uidb64 = user_extract_uidb64(token=token)

    user = user_check_token(uidb64=uidb64, token=token_user)

    if new_password != password_confirm:
        raise ValidationError("Contraseñas no coinciden")

    # Validar contraseña con las respectivas limitaciones.
    # UserAttributeSimilarityValidator
    # MinimumLengthValidator
    # CommonPasswordValidator
    # NumericPasswordValidator
    validate_password(password=new_password, user=user.email)

    user.set_password(new_password)
    user.save(update_fields=["password"])

    return user


def user_password_change(*, user_id:int, old_password:str, new_password:str, password_confirm):
    user = user_by_id(id=user_id)

    if new_password != password_confirm:
        raise ValidationError("Contraseñas no coinciden.")
    
    # Validar si la contraseña enviada es válida
    if not user.check_password(old_password):
        raise ValidationError("Contraseña anterior no es válida.")

    validate_password(password=new_password, user=user)
    user.set_password(new_password)
    user.save(update_fields=["password"])

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

    return user


# =================
# Services methods
# =================

def user_extract_uidb64(*, token: str) -> str:
    separator = '_'
    try:
        # Remover espacios en blanco
        token_strip = token.strip()
        # Encontrar separador
        extract_uidb64 = token_strip.find(separator)
        if not extract_uidb64 != -1:
            raise ValidationError('Código inválido.')

        return token[extract_uidb64 + 1:]

    except:
        raise ValidationError('Código inválido.')


def user_extract_token(*, token: str) -> str:
    separator = '_'
    try:
        # Remover espacios en blanco del token.
        token_strip = token.strip()
        # Encontrar el separador dentro del token. 
        extract_token = token_strip.find(separator)
        if not extract_token != -1:
            raise ValidationError('Código inválido.')

        return token[:extract_token]

    except Exception:
        raise ValidationError('Código inválido.')


def user_check_token(*, uidb64: int, token: str) -> BaseUser:
    """función que permite chequear el token de la cadena enviada.

    Parámetros:
    uidb64 Código de id extraido
    token Código de usuario enviado en la petición
    """
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = user_by_id(id=user_id)

    # Si el token no esta relacionado al usuario envia error.
    if not PasswordResetTokenGenerator().check_token(user, token):
        raise ValidationError('Invalid code.')

    return user


def user_make_token(*, email:int):
    """Servicio que permite crear un token aleatorio con fecha
    de caducidad detallado en las configuraciones a partir del
    email del usuario.
    """
    separator = "_"
    user = user_by_email(email=email)

    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)

    return "%s%s%s" % (token, separator,uidb64 )

