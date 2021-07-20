from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
from server.users.services import user_create
from server.users.models import BaseUser



class TestUserLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:auth:login')
    
    def test_api_empty_data(self):
        # Si se envía data vacía a la api debería dar error.
        # Api responde con estado 400
        response = self.client.post(self.url, {})
        self.assertEqual(400, response.status_code)
    
    def test_api_credentials_invalid(self):
        # Envío de credenciales no válidas a la api.
        data = {
            'email': fake.email(),
            'password': fake.password()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)
    
    def test_api_with_valid_data_but_not_verify_phone(self):
        # Si se registra correctamente un usuario e intenta acceder a la
        # session sin haber confirmado el código enviado a su número celular
        # la api respondera con estado 401 de credenciales inválidas.
        email =  fake.email(),
        password = fake.password()
        data = {
            'first_name':fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': password,
            'avatar': None
        }
        user_create(**data)
        self.assertEqual(1, BaseUser.objects.count())

        credentials = {
            'email':email,
            'password': password
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(401, response.status_code)
        

    
