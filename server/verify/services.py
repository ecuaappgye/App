from django.conf import settings
from twilio.rest import Client

from .models import CallbackToken


def send_token(*, user_id:int, alias_type, token_type):
    token = CallbackToken.objects.create(user_id = user_id,
                type = alias_type.upper())
    send_sms_for_user(phone='+593969164843', content=f'Verifica tu cuenta {token.key}')
    
def send_sms_for_user(*, phone:str, content:str):
    client = Client(settings.SMS_ACCOUNT_SID, settings.SMS_AUTH_TOKEN)
    message = client.messages.create(
        to=phone,
        from_= settings.SMS_TWILIO_NUMBER,
        body = content 
    )
    
    return message
