from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.selectors import user_by_id
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser



class UserByIdTest(TestCase):
    def setUp(self):
        self.selector = user_by_id
    
    @ patch('server.users.selectors.user_by_id')
    # Testeando el selector cuando un usuario no es encontrado.
    def test_selector_with_user_not_souch_found(self, user_by_id_mock):
        with self.assertRaises(ValidationError):
            self.selector(id=fake.random_digit())
        
    @ patch('server.users.selectors.user_by_id')
    # Testeando el selector cuando un usuario es encontrado
    # Se aplica fábricas en las pruebas
    def test_selector_with_user_found(self, user_by_id_mock):
        BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())
        self.selector(id=BaseUser.objects.first().id)




    


