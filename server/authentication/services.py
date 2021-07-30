from typing import Iterator

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from server.users.selectors import user_by_id
from twilio.rest import Client

from .models import CallbackToken
from .selectors import callback_token_by_user_id
from .utils import validate_phone_format, validate_token


def user_create_verify(*, user_id: int, phone: str, ip_address:str=None, user_agent:str=None):
    """Servicio que permite realizar el registro del token 
    generado y posteriormente el envío del mismo a traves
    del servicio de mensajería de Twilio.

    Parámetros:
    user_id  -> Identificador del usuario al que vamos a enlazar.
    phone -> Número telefónico
    ip_address -> Dirección IP del dispositivo de la petición.
    user_agent -> Usuario de la petición del dispositivo.
    """
    validate_phone_format(phone=phone)

    callback_token_data = {
        'user_id': user_id, 
        'alias_type': 'mobile',
        'token_type': CallbackToken.TOKEN_TYPE_AUTH,
        'ip_address': ip_address,
        'user_agent': user_agent
    }

    token = create_token_callback_for_user(data=callback_token_data)
    invalidate_previous_tokens(callback_token=token)
    send_sms_with_callback_token(phone=phone, key=token.key)


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
    validate_token(token=token, token_compare=token_user)
    validate_token_age(callbacktoken=token_user)

    user = user_by_id(id=user_id)
    user.is_active = True
    user.save(update_fields=['is_active'])

    return token_user


def send_sms_with_callback_token(*, phone: str, key: str):
    """Función que permite realizar el envío de mensajes utilizando
    el servicio de Twilio.

    Parámetros:
    phone -> Número de teléfono a enviar.
    key -> Código generado.
    """
    client = Client(settings.SMS_ACCOUNT_SID, settings.SMS_AUTH_TOKEN)
    # message = client.messages.create(body=settings.VERIFY_MOBILE_MESSAGE % key,
    #                                  from_=settings.SMS_TWILIO_NUMBER,
    #                                  to='+593969164843')
                                    
    # return 'message'


def invalidate_previous_tokens(*, callback_token: CallbackToken) -> Iterator[CallbackToken]:
    """Cuando se emite un nuevo hay que desactivar todos los
    token relacionados con ese usuario.

    Parámetros:
    callback_token -> Instancia del modelo de callback tokens.
    """
    tokens = CallbackToken.objects.active().filter(user_id=callback_token.user.id, 
                        type=callback_token.type).exclude(id=callback_token.id)
    if not tokens:
        return None

    tokens.update(is_active=False)

    return tokens


def validate_token_age(*, callbacktoken: CallbackToken):
    """Permite determinar si un token determinado a caducado.

    Parámetros:
    callbacktoken -> Instancia del token del usuario.
    """
    try:

        token = CallbackToken.objects.get(key=callbacktoken.key, is_active=True)
        seconds = (timezone.now() - token.created_at).total_seconds()
        token_expiry_time = settings.VERIFY_TOKEN_EXPIRE_TIME

        # Segundos trasncurrido desde el envío del token supera el vencimiento.
        if seconds >= token_expiry_time:
            raise ValidationError(settings.VERIFY_TOKEN_EXPIRED_MESSAGE)
        # Desactivar el token.
        # Token con atributo is active en False 
        token.is_active = False
        token.save(update_fields=['is_active'])

        return token

    except CallbackToken.DoesNotExist:
        return None


def create_token_callback_for_user(*, data):    
    token = CallbackToken(user_id=data.get('user_id'),
                          to_alias_type=data.get('alias_type').upper(),
                          to_alias=data.get('alias_type'),
                          type=data.get('token_type'),
                          user_agent=data.get('user_agent'),
                          ip_address=data.get('ip_address'))
    token.save()

    return token

