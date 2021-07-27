from django.dispatch import receiver
from django.db.models import signals
from .models import CallbackToken


@receiver(signals.pre_save, sender=CallbackToken)
def check_unique_token(sender, instance, **kwargs):
    if instance._state.adding:
        # pass hoy
