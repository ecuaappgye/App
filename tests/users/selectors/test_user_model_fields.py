from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.selectors import user_model_fields, user_data
from server.users.models import BaseUser
from server.users.factories import BaseUserFactory




class UserByIdTest(TestCase):
    def setUp(self):
        self.selector = user_model_fields
    
    @ patch('server.users.selectors.user_data')
    def test_selector_with_user_data_not_valid(self, user_data_mock):
        with self.assertRaises(ValidationError):
            self.selector(user_data=None)

    @ patch('server.users.selectors.user_data')
    def test_selector_return_data(self, user_data_mock):
        BaseUserFactory()
        user=user_data(user=BaseUser.objects.first())
        self.selector(user_data=user)

        
    