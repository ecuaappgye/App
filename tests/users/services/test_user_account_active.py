from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_account_active
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserAccountActive(TestCase):
    def setUp(self):
        self.service = user_account_active
    
    @ patch('server.users.services.user_account_active')
    def test_service_with_user_not_souch_found(self, user_account_active_mock):
        credentials = {'email': fake.email(), 'password':fake.password()}
        result = self.service(credentials=credentials)
        self.assertIsNone(result)

    @ patch('server.users.services.user_account_active')
    def test_service_with_user_active(self, user_account_active_mock):
        email, password = fake.email(), fake.password()
        BaseUserFactory(email=email, password=password, is_active=True)
        credentials = {'email': email , 'password': password }
        self.service(credentials=credentials)

    @ patch('server.users.services.user_account_active')
    def test_service_with_account_not_active_raise_validation_error(self, user_account_active_mock):
        email, password = fake.email(), fake.password()
        BaseUserFactory(email=email, password=password)
        credentials = {'email': email , 'password': password }
        with self.assertRaises(ValidationError):
            self.service(credentials=credentials)