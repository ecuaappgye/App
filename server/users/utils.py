import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
 


def validate_password(*, password:str, user):
    errors = dict()
    try:
        validators.validate_password(password=password, user=user)
    except Exception as e:
        errors["password"] = list(e.messages)
    
    if errors:
        raise ValidationError(errors)




