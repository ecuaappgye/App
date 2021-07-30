from collections import OrderedDict
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class TestUserGetApi(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_api_without_credentials(self):
        # La api requiere de credenciales de autenticación.
        # Sino encunetra la sessión responde con error.
        user = BaseUserFactory()
        response = self.client.get(reverse('api:auth:get', kwargs={'user_id': user.id}))
        self.assertEqual(403, response.status_code)
    
    def test_api_with_credentials_and_user_not_souch_found(self):
        # La api requiere de credenciales de autenticación.
        # Si se envía un usuario identificador no válido la api
        # retorna un estado de error.
        email, password= fake.email(), fake.password()
        BaseUserFactory(email=email, password=password)
        self.client.login(email=email, password=password)

        response = self.client.post(reverse('api:auth:get', kwargs={'user_id': fake.random_digit()}))
        self.assertEqual(403, response.status_code)
    
    def test_api_return_data(self):
        # La api debe retornar un estado aceptado y enviar en un objeto
        # JSON el cual debe tener asociada la información.
        # Usuario tiene una estructura determinada

        # 'id': user.id, 
        # "first_name": user.first_name,
        # "last_name": user.last_name,
        # "email": user.email,
        # "address": user.address,
        # "cdi": user.cdi,
        # "phone": user.phone
        
        email, password= fake.email(), fake.password()
        user = BaseUserFactory(email=email, password=password, is_active=True)
        is_logged = self.client.login(email=email, password=password)
        self.assertTrue(is_logged)
        
        response = self.client.get(reverse('api:auth:get', kwargs={'user_id': user.id}))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.data)

        expect = OrderedDict(
            [('id', user.id),
             ('first_name', user.first_name),
             ('last_name', user.last_name),
             ('email', user.email),
             ('cdi', user.cdi),
             ('phone', user.phone),
             ('address', user.address)])
        self.assertEqual(expect, OrderedDict(response.data))