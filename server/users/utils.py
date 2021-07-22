import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from server.communication.managers import CommunicationDispatcher
from twilio.rest import Client
from django.conf import settings
from datetime import datetime
 

PASSWORD_RESET_EVENT_CODE = "PASSWORD_RESET"
PASSWORD_RESET_CHECK_EVENT_CODE = "PASSWORD_RESET_CHECK"
PASSWORD_CHANGE_EVENT_CODE = "PASSWORD_CHANGE"
EMAIL_CHANGE_EVENT_CODE = "EMAIL_CHANGE"

def send_email_password_reset_for_user(user, extra_context):
    messages = CommunicationDispatcher().get_messages(PASSWORD_RESET_EVENT_CODE, extra_context)
    CommunicationDispatcher().dispatch_user_messages(user, messages)

def send_email_password_reset_check_for_user(user, extra_context):
    messages = CommunicationDispatcher().get_messages(PASSWORD_RESET_CHECK_EVENT_CODE,
            extra_context)
    CommunicationDispatcher().dispatch_user_messages(user, messages)

def send_email_password_change(user, extra_context):
    messages = CommunicationDispatcher().get_messages(PASSWORD_CHANGE_EVENT_CODE,
            extra_context)
    CommunicationDispatcher().dispatch_user_messages(user, messages)

def send_email_email_change(user, extra_context):
    messages = CommunicationDispatcher().get_messages(EMAIL_CHANGE_EVENT_CODE,
            extra_context)
    CommunicationDispatcher().dispatch_user_messages(user, messages)

def send_sms_for_user(*, phone:str, content:str):
    client = Client(settings.SMS_ACCOUNT_SID, settings.SMS_AUTH_TOKEN)
    message = client.messages.create(
        to=phone,
        from_= settings.SMS_TWILIO_NUMBER,
        body = content 
    )
    
    return message
    

def validate_password(*, password:str, user):
    errors = dict()
    try:
        validators.validate_password(password=password, user=user)
    except Exception as e:
        errors["password"] = list(e.messages)
    
    if errors:
        raise ValidationError(errors)


def user_directory_path(instance, filename):
    now = datetime.now()
    format = now.strftime('%Y-%m-%d %H:%M:%S')

    return f'avatar/{format}-{filename}'
