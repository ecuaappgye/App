from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.selectors import user_by_id_data
from server.users.factories import BaseUserFactory
from collections import OrderedDict


class UserByIdTest(TestCase):
    def setUp(self):
        self.selector = user_by_id_data
    
    @ patch('server.users.selectors.user_by_id_data')
    def test_selector_with_user_not_souch_found(self, user_by_id_data_mock):
        with self.assertRaises(ValidationError):
            self.selector(id=fake.random_digit())

    @ patch('server.users.selectors.user_by_id_data')
    def test_selector_return_data(self, user_by_id_data_mock):
        # El selector devuelve en formato json la información
        # harcodeada del usuario.
        user = BaseUserFactory()
        result = self.selector(id=user.id)

        expect = OrderedDict([
            ('id', user.id),
            ('first_name', user.first_name),
            ('last_name', user.last_name),
            ('email', user.email),
            ('address', user.address),
            ('avatar', user.avatar.url if user.avatar else None),
            ('cdi', user.cdi),
            ('phone', user.phone)])

        self.assertEqual(expect, OrderedDict(result))