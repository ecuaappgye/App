from server.authentication.models import CallbackToken
from server.users.models import BaseUser
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_password_reset
from server.users.factories import BaseUserFactory


class UserPasswordReset(TestCase):
    def setUp(self):
        self.service = user_password_reset
    
    @ patch('server.users.services.user_password_reset')
    def test_service_with_user_not_souch_found(self, user_password_reset_mock):
        # Servicio debe enviar un error cuando se envía un correo electrónico
        # no encontrado en el módulo de usuarios.
        with self.assertRaises(ValidationError):
            data = {
                'email':fake.email(),
                'ip_address' :fake.ipv4(),
                'user_agent' :fake.user_agent()
            }
            self.service(**data)

    @ patch('server.users.services.user_password_reset')
    def test_service_with_success_and_call_event(self, send_email_password_reset_for_user_mock):
        BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        data = {
            'email': BaseUser.objects.first().email, 
            'ip_address' :fake.ipv4(),
            'user_agent' :fake.user_agent()
        }
        self.service(**data)

    @ patch('server.users.services.user_password_reset')
    def test_service_with_invalidated_tokens_with_multiples_request(self, 
            send_email_password_reset_for_user_mock):
        # El servicio debería invalidar tokens cada vez que se pide un
        # nuevo token para ese usuario en particular.
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())
        data = {
            'email': BaseUser.objects.first().email, 
            'ip_address' :fake.ipv4(),
            'user_agent' :fake.user_agent()
        }
        self.service(**data)
        self.assertEqual(1, CallbackToken.objects.count())
        # Envío de una nueva petición teniendo ya un token asignado.
        # Servicio debería deshabilitar los tokens activos a este usuario
        # teniendo en cuenta el tipo de token. (TOKEN_AUTH, TOKEN_VERIFY,
        # TOKEN_PASSWORD_RESET)
        self.service(**data)
        self.assertEqual(2, CallbackToken.objects.count())
        self.assertTrue(1, CallbackToken.objects.filter(user_id=user.id, is_active=True).count())