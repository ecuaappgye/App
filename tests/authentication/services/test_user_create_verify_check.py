from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.authentication.models import CallbackToken
from server.authentication.services import user_create_verify_check, user_create_verify
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserCreate(TestCase):
    def setUp(self):
        self.service = user_create_verify_check

    @ patch('server.authentication.services.user_create_verify_check')
    def test_service_with_user_not_souch_found(self, user_create_verify_check_mock):
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(), token=fake.random_number(digits=6))
    
    @ patch('server.authentication.services.user_create_verify_check')
    def test_service_with_token_none(self, user_create_verify_check_mock):
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id, token=None)
    
    @ patch('server.authentication.services.user_create_verify_check')
    def test_service_with_invalid_code(self, user_create_verify_check_mock):
        # El servicio se asegura que el código recibido sea correcto.
        # El servicio se asegura de enviar error.
        user = BaseUserFactory()

        data = {
            'user_id' : user.id,
            'phone': fake.bothify(text='+593#########'),
            'ip_address' :fake.ipv4(),
            'user_agent' :fake.user_agent()
        }
        user_create_verify(data)
        self.assertEqual(1, CallbackToken.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id,token=fake.random_number(digits=6))
    
    @ patch('server.authentication.services.validate_token_age')
    def test_service_with_valid_token_and_active_account_user(self, validate_token_age_mock):
        # El servicio activa la cuenta del usuario una vez que se ha enviado el token
        # correcto. El atributo del usuario de ´is_active´ pasa a True para poder permitir
        # el inicio de sesión.
        user = BaseUserFactory()

        data = {
            'user_id' : user.id,
            'phone': fake.bothify(text='+593#########'),
            'ip_address' :fake.ipv4(),
            'user_agent' :fake.user_agent()
        }

        user_create_verify(data)
        self.assertEqual(1, CallbackToken.objects.count())

        self.service(user_id=user.id, token=CallbackToken.objects.first().key)
        self.assertTrue(BaseUser.objects.first().is_active)
        self.assertTrue(validate_token_age_mock.called)