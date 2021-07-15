import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from server.communication.managers import CommunicationDispatcher
 

PASSWORD_RESET_EVENT_CODE = "PASSWORD_RESET"

def send_email_password_reset_for_user(*, user, extra_context):
    messages = CommunicationDispatcher().get_messages(PASSWORD_RESET_EVENT_CODE, extra_context)
    CommunicationDispatcher().dispatch_user_messages(user, messages)
    
def validate_password(*, password:str, user):
    errors = dict()
    try:
        validators.validate_password(password=password, user=user)
    except Exception as e:
        errors["password"] = list(e.messages)
    
    if errors:
        raise ValidationError(errors)




