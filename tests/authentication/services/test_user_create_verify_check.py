from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.authentication.models import CallbackToken
from server.authentication.services import user_create_verify_check
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserCreate(TestCase):
    def setUp(self):
        self.service = user_create_verify_check

    @ patch('server.authentication.services.user_create_verify_check')
    def test_service_with_user_not_souch_found(self, user_create_verify_check_mock):
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(), token=fake.random_number(digits=3))
    
    @ patch('server.authentication.services.user_create_verify_check')
    def test_service_with_token_none(self, user_create_verify_check_mock):
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id, token=None)