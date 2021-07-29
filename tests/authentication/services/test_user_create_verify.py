from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.authentication.models import CallbackToken
from server.authentication.services import user_create_verify
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserCreate(TestCase):
    def setUp(self):
        self.service = user_create_verify

    @ patch('server.authentication.services.user_create_verify')
    def test_service_with_user_not_souch_found(self, user_create_verify_mock):
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(),
                        phone=fake.phone_number(),
                        ip_address=fake.ipv4(),
                        user_agent=fake.user_agent())
    
    @ patch('server.authentication.services.user_create_verify')
    def test_service_with_phone_none(self, user_create_verify_mock):
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(), phone=None)

    @ patch('server.authentication.services.user_create_verify')
    def test_service_with_number_phone_invalid_format(self, user_create_verify_mock):
        # Servicio valida que el número telefónico este regido al formato ´+593..´
        # Servicio envia error en el caso del formato no válido.
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id,
                         phone=fake.phone_number(),
                         ip_address=fake.ipv4(),
                         user_agent=fake.user_agent())

    @ patch('server.authentication.services.send_sms_with_callback_token')
    def test_service_with_success(self, send_sms_with_callback_token_mock):
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        self.service(user_id=user.id,
                     phone=fake.bothify(text='+593#########'),
                     ip_address=fake.ipv4(),
                     user_agent=fake.user_agent())
        self.assertEqual(1, CallbackToken.objects.count())
        self.assertTrue(send_sms_with_callback_token_mock.called)
    
    @ patch('server.authentication.services.send_sms_with_callback_token')
    def test_service_with_token_previous_validate(self, send_sms_with_callback_token_mock):
        # Si un usuario ya ha sido notificado con un código el servicio debería
        # invalidar los token previos.
        user = BaseUserFactory()
        self.service(user_id=user.id, 
                     phone=fake.bothify(text='+593#########'),
                     ip_address=fake.ipv4(),
                     user_agent=fake.user_agent())
        self.assertTrue(CallbackToken.objects.first().is_active)
        self.assertTrue(send_sms_with_callback_token_mock.called)
        # Servicio proporciona un nuevo token (código) e invalida los previos.
        self.service(user_id=user.id, 
                     phone=fake.bothify(text='+593#########'),
                     ip_address=fake.ipv4(),
                     user_agent=fake.user_agent())
        self.assertTrue(send_sms_with_callback_token_mock.called)
        self.assertEqual(2,  CallbackToken.objects.count())
        #self.assertFalse(CallbackToken.objects.last().is_active)