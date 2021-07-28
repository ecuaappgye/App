from collections import OrderedDict
from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
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
        # credeciales.
        # En ésta prueba se simula el proceso de haber confirmado el 
        # código enviado al celular.
        # El campo ´is_active´ en True permite simular este proceso.
        # En el caso de que esté en False ésta prueba falla.
        email =  fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password, is_active=True)
        credentials = {'email':email, 'password': password}
        response = self.client.post(self.url, credentials)
        self.assertEqual(200, response.status_code)
        # Iniciar sesión con credenciales dclsel mismo usuario
        response_already_login = self.client.post(self.url, credentials)
        self.assertEqual(409, response_already_login.status_code)
        self.assertEqual(0, Session.objects.count())

    def test_api_with_invalid_credentials(self):
        # Si un usuario envía credenciales inválidas no permite acceso.
        # Api responde con estado 401
        email =  fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password, is_active=True)
        
        credentials = {
            'email': fake.email(),
            'password': fake.password
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(401, response.status_code)
    
    def test_api_with_valid_credentials_and_return_current_session_with_user(self):
        # Probando que la api responda con con estado correcto.
        # La api debe retornar la sesión del usuario y la respectiva
        # información en formato JSON.
        email =  fake.email()
        password = fake.password()
        user = BaseUserFactory(email=email, password=password, is_active=True)
        credentials = {
            'email': email,
            'password': password
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(200, response.status_code)
        # Una vez que se haya registrado un usuario debería almacenar
        # la sesión como única y con una fecha de registro.
        self.assertEqual(1, Session.objects.count())
        # Obtener la sesión de la base de datos y comparar si coincide
        # con la sesión devuelta por el usuario.
        session = Session.objects.first().session_key
        current_session = response.data.get('session')
        self.assertEqual(session, current_session)
        # Obtener los datos retornados relacionado con la información
        # del usuario en sesión y verificar el formato.
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

        self.assertEqual(expect, OrderedDict(response.data.get('data')))
