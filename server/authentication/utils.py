import re
import string

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


def generate_numeric_token():
    """Genera un cadena string con una longitud máxima de 6 dígitos.
    En el modelo se emite una señal (signal) que se activa antes de
    registrar el token.
    """
    return get_random_string(length=6, allowed_chars=string.digits)

def validate_phone_format(*, phone):
    if not phone:
        raise ValidationError(settings.VERIFY_PHONE_FORMAT_INVALID)
        
    if not re.match(r'^\+593\d{1,12}$', phone):
        raise ValidationError(settings.VERIFY_PHONE_FORMAT_INVALID)
    
    return phone
