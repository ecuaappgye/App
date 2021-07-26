from django.conf import settings
from django.core.exceptions import ValidationError
from twilio.rest import Client

from .models import CallbackToken
from .selectors import callback_token_by_user_id
from server.users.selectors import user_by_id


def user_create_verify(*, user_id: int, phone: str):
    """Servicio que permite realizar el registro del token 
    generado y posteriormente el envío del mismo a traves
    del servicio de mensajería de Twilio.

    Parámetros:
    user_id  -> Identificador del usuario al que vamos a enlazar.
    phone -> Número telefónico
    """
    token = create_token_callback_for_user(user_id=user_id,
                                           alias_type='mobile',
                                           token_type='AUTH')
    print(token)

    #send_sms_with_callback_token(phone=phone, content='content')


def user_create_verify_check(*, user_id: int, token: str):
    """Servicio que permite realizar la verificación del token 
    enviado al usuario. Básicamente se compara si ese token 
    aún está disponible y si es válido para ese usuario en 
    particular.

    Parámetros:
    user_id  -> Identificador del usuario al que vamos a enlazar.
    token -> Código de verificación enviado al móvil.
    """
    token_user = callback_token_by_user_id(id=user_id)
    if token != token_user.key:
        raise ValidationError('Código no válido.')

    user = user_by_id(id=user_id)
    user.is_active = True
    user.save(update_fields=['is_active'])

    token_user.is_active = False
    token_user.save(update_fields=['is_active'])

    return token_user


def create_token_callback_for_user(*, user_id, alias_type, token_type):
    token = CallbackToken(user_id=user_id,
                          to_alias_type=alias_type.upper(),
                          to_alias=alias_type, type=token_type)
    token.save()

    return token


def send_sms_with_callback_token(*, phone: str, content):
    """Función que permite realizar el envío de mensajes utilizando
    el servicio de Twilio.
    """
    client = Client(settings.SMS_ACCOUNT_SID, settings.SMS_AUTH_TOKEN)
    message = client.messages.create(
        to='+593969164843',
        from_=settings.SMS_TWILIO_NUMBER,
        body=content
    )

    return message
