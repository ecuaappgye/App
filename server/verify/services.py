from django.utils.crypto import get_random_string
import string


def generate_numeric_token():
    # Genera un cadena string con una longitud máxima de 6 dígitos.
    return get_random_string(length=6, allowed_chars=string.digits)

def send_token(*, user, alias_type, token_type):
    pass

