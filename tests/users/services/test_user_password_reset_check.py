from server.authentication.models import CallbackToken
from server.users.models import BaseUser
from unittest.mock import Base, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_password_reset_check, user_password_reset
from server.users.factories import BaseUserFactory


class UserPasswordResetCheck(TestCase):
    def setUp(self):
        self.service = user_password_reset_check
    
    @ patch('server.users.services.user_password_reset_check')
    def test_service_with_password_not_match(self, user_password_reset_check_mock):
        # Servicio debería responder con error cuando se emite un token válido
        # pero las contraseñas de confirmación no coinciden.
        user = BaseUserFactory()
        password_reset_data={
            'email': user.email,
            'ip_address' :fake.ipv4(),
            'user_agent' :fake.user_agent()
        }
        token = user_password_reset(**password_reset_data)
        self.assertEqual(1, CallbackToken.objects.count())

        data = {
            'token': token.key,
            'new_password': fake.password(),
            'password_confirm': fake.password()
        }
        with self.assertRaises(ValidationError):
            self.service(**data)
    
    @ patch('server.users.services.user_password_reset_check')
    def test_service_with_callback_token_not_found(self, user_password_reset_check_mock):
        password = fake.password()
        data = {
            'token': fake.random_number(digits=6),
            'new_password': password,
            'password_confirm': password
        }
        with self.assertRaises(ValidationError):
            self.service(**data)
    
    @ patch('server.users.services.user_password_reset_check')
    def test_service_with_callback_token_none(self, user_password_reset_check_mock):
        password = fake.password()
        data = {
            'token': None,
            'new_password': password,
            'password_confirm': password
        }
        with self.assertRaises(ValidationError):
            self.service(**data)

    @ patch('server.users.services.user_password_reset_check')
    def test_service_with_callback_token_invalid(self, user_password_reset_check_mock):
        user = BaseUserFactory()
        password_reset_data={
            'email': user.email,
            'ip_address' : fake.ipv4(),
            'user_agent' : fake.user_agent()
        }
        user_password_reset(**password_reset_data)

        data = {
            'token': fake.random_number(digits=6),
            'new_password': fake.password(),
            'password_confirm': fake.password()
        }
        with self.assertRaises(ValidationError):
            self.service(**data)
    
    @ patch('server.users.services.user_password_reset_check')
    def test_service_with_vulnerable_password(self, user_password_reset_check_mock):
        user = BaseUserFactory()
        password_reset_data={
            'email': user.email,
            'ip_address' : fake.ipv4(),
            'user_agent' : fake.user_agent()
        }
        token = user_password_reset(**password_reset_data)

        vulnerable_password = fake.password(length=5, digits=False)
        data = {
            'token': token.key,
            'new_password': vulnerable_password,
            'password_confirm': vulnerable_password
        }
        with self.assertRaises(ValidationError):
            self.service(**data)
        
    @ patch('server.users.services.user_password_reset_check')
    def test_service_success(self, user_password_reset_check_mock):
        user = BaseUserFactory()
        password_reset_data={
            'email': user.email,
            'ip_address' : fake.ipv4(),
            'user_agent' : fake.user_agent()
        }
        token = user_password_reset(**password_reset_data)

        password = fake.password()
        data = {
            'token': token.key,
            'new_password': password,
            'password_confirm': password
        }
        self.service(**data)
        self.assertTrue(BaseUser.objects.first().has_usable_password())

