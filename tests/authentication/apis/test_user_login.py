from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
from server.users.services import user_create
from server.users.models import BaseUser
from server.users.factories import BaseUserFactory
from django.contrib.sessions.models import Session


class TestUserLoginApi(TestCase):
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
        email =  fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)
        self.assertEqual(1, BaseUser.objects.count())

        credentials = {
            'email':email,
            'password': password
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(401, response.status_code)
    
    def test_api_with_already_session(self):
        # Si un usuario ha iniciado sessión con anterioridad y su
        # sesión aun continúa activa la api no deberá permitir el 
        # acceso y deberá responder 409 conflicto.
        # Elimina la sesión del usuario actualmente logueado con esas
        # crendeciales.
        email =  fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)
        
        # momentaneo =========================
        x = BaseUser.objects.first()
        x.is_active = True
        x.save()

        credentials = {
            'email':email,
            'password': password
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(200, response.status_code)

        # Iniciar sesión con credenciales del mismo usuario
        response_already_login = self.client.post(self.url, credentials)
        self.assertEqual(409, response_already_login.status_code)
        self.assertEqual(0, Session.objects.count())

    def test_api_with_invalid_credentials(self):
        # Si un usuario envía credenciales inválidas no permite acceso.
        # Api responde con estado 401
        email =  fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)
        
        # momentaneo =========================
        x = BaseUser.objects.first()
        x.is_active = True
        x.save()

        crendentials = {
            'email': fake.email(),
            'password': fake.password
        }
        response = self.client.post(self.url, crendentials)
        self.assertEqual(401, response.status_code)





        

    
