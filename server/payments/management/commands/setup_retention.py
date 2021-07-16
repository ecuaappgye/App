from django.core.management.base import BaseCommand
from django.db import models
from server.payments.models import Retention

class Command(BaseCommand): 
    def handle(self, *args, **kargs):
        Retention.objects.create(
            service_total = 8,
            service_supervisor = 5,
            service_app = 95
        )


