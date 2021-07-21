from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.users.selectors import user_data
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser
from collections import OrderedDict



class UserByIdTest(TestCase):
    def setUp(self):
        self.selector = user_data
    
    @ patch('server.users.selectors.user_data')
    def test_selector_with_user_not_valid(self, user_data_mock):
        with self.assertRaises(ValidationError):
            self.selector(user=None)
    
    @ patch('server.users.selectors.user_data')
    def test_selector_found_user_and_return_data(self, user_data_mock):
        BaseUserFactory()
        user = BaseUser.objects.first()

        expect = OrderedDict(
            [('id', user.id),
             ('first_name', user.first_name),
             ('last_name', user.last_name),
             ('email', user.email),
             ('address', user.address),
             ('avatar', user.avatar.url if user.avatar else None),
             ('cdi', user.cdi),
             ('phone', user.phone)])
        
        result = self.selector(user=user)
        self.assertEqual(expect, OrderedDict(result))