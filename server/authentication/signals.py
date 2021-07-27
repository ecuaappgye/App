from django.core.exceptions import ValidationError
from server.authentication.utils import generate_numeric_token
from django.dispatch import receiver
from django.db.models import signals
from .models import CallbackToken
from django.conf import settings


@receiver(signals.pre_save, sender=CallbackToken)
def check_unique_token(sender, instance, **kwargs):
    if instance._state.adding:
        unique = False
        if not isinstance(instance, CallbackToken):
            return None
        
        tokens = CallbackToken.objects.filter(key=instance.key, is_active=True).exists()
        tries = 0
        if tokens:
            while tries < settings.VERIFY_TOKEN_GENERATION_ATTEMPTS:
                tries = tries+1
                refresh_key = generate_numeric_token()
                instance.key = refresh_key

                if not CallbackToken.objects.filter(key=instance.key, is_active=True).exists():
                    unique = True
                    break
            
            if not unique:
                raise ValidationError('El token no pudo ser creado como único.')




