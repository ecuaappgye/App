from server.users.models import BaseUser
from django.core.management.base import BaseCommand
from django.core import management
from subprocess import call
import logging


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.info("Database cleaning")
        management.call_command('flush')
        BaseUser.objects.create_superuser(first_name='italo',
                        last_name='Barzola',email='italobarzola18@gmail.com',
                        password='12345marcos')

