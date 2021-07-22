from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_email_change
from server.users.models import BaseUser
from server.users.factories import BaseUserFactory


class UserEmailChange(TestCase):
    def setUp(self):
        self.service = user_email_change
    
    @ patch('server.users.services.user_email_change')
    def test_service_with_user_not_souch_found(self, user_email_change_mock):
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(), email=fake.email())

    @ patch('server.users.services.user_email_change')
    def test_service_with_email_already_exists(self, user_email_change_mock):
        # El servicio debería no permitir el registro de un correo electrónico
        # que ya se encuentre actualizado.
        first_user = BaseUserFactory()
        # Creación de otro usuario para actualizar correo electrónico.
        second_user = BaseUserFactory()
        # Invocar el servicio con un email ya existente
        with self.assertRaises(ValidationError):
            self.service(user_id=second_user.id, email=first_user.email)

    @ patch('server.users.services.user_email_change')
    def test_service_with_email_not_format(self, user_email_change_mock):
        # Servicio responde con error cuando no se envía un correo eletrónico válido.
        user = BaseUserFactory()
        with self.assertRaises(ValidationError):
            self.service(user_id=user.id, email=fake.first_name())

    @ patch('server.users.services.user_email_change')
    def test_service_success(self, user_email_change_mock):
        email = fake.email()
        user = BaseUserFactory()
        self.service(user_id=user.id, email=email)
        # Confirmar de que el usuario ha mutado su email.
        self.assertEqual(email, BaseUser.objects.first().email)
    



    
