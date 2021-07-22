from collections import OrderedDict
from unittest.mock import patch

from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser
from server.users.services import user_update_profile


class TestUserUniqueSession(TestCase):
    def setUp(self):
        self.service = user_update_profile
    
    @ patch('server.users.services.user_update_profile')
    def test_service_with_user_not_souch_found(self, user_update_profile_mock):
        # Servicio no retorna usuario encontrado
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(), data={})

    @ patch('server.users.services.user_update_profile')
    def test_service_with_empty_data(self, user_update_profile_mock):
        # El servicio envía error cuando no se han enviado datos para
        # realizar actualizaciones sobre ese usuario determinado.
        user = BaseUserFactory()
        with self.assertRaises(ValidationError):
            self.service(user_id=user.id, data={})

    @ patch('server.users.services.user_update_profile')
    def test_service_with_data_not_allowed_to_update(self, user_update_profile_mock):
        # El servicio retorna ´None´ cuando no hay campos para actualizar.
        # Si se envían datos no permitidos este no actualizará el registro.
        user = BaseUserFactory()
        data = {'email':fake.email()}
        result = self.service(user_id=user.id, data=data)
        self.assertIsNone(result)
    
    @ patch('server.users.services.user_update_profile')
    def test_service_with_allowed_data_and_success(self, user_update_profile_mock):
        user = BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())

        user_data = OrderedDict(
            [('id', user.id),
             ('first_name', user.first_name),
             ('last_name', user.last_name),
             ('email', user.email),
             ('address', user.address),
             ('avatar', user.avatar.url if user.avatar else None),
             ('cdi', user.cdi),
             ('phone', user.phone)])
        
        data = {
            'phone': fake.ean(prefixes=('0'),length=8),
            'cdi': fake.ean(prefixes=('0'), length=8)
        }
        self.service(user_id=user.id, data=data)

        user_updated = BaseUser.objects.first()
        user_updated_data = OrderedDict(
            [('id', user_updated.id),
             ('first_name', user_updated.first_name),
             ('last_name', user_updated.last_name),
             ('email', user_updated.email),
             ('address', user_updated.address),
             ('avatar', user_updated.avatar.url if user.avatar else None),
             ('cdi', user_updated.cdi),
             ('phone', user_updated.phone)])
        
        self.assertNotEqual(user_updated_data, user_data)
        






    


