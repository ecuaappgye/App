from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from server.common.test_utils import fake
from server.users.services import user_password_reset
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserPasswordReset(TransactionTestCase):
    def setUp(self):
        self.service = user_password_reset
    
    @ patch('server.users.services.user_password_reset')
    def test_service_with_user_not_souch_found(self, user_password_reset_mock):
        # Servicio debe enviar un error cuando se envía un correo electrónico
        # no encontrado en el módulo de usuarios.
        with self.assertRaises(ValidationError):
            self.service(email=fake.email())

    @ patch('server.users.services.user_password_reset')
    def test_service_with_success_and_call_event(self, send_email_password_reset_for_user_mock):
        BaseUserFactory()