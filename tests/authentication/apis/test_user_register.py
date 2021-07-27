from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse


class TestUserLoginApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:auth:register')

    def test_api_with_empty_data(self):
        # Probando la api enviando data vacía.
        # Api debe responder con un estado no válido.
        response = self.client.post(self.url, {})
        self.assertEqual(400, response.status_code)
    
    def test_api_and_not_active_account(self):
        # Cuando un usuario se registra, éste deberá activar su cuenta.
        # Necesariamente debería activar su cuenta mediante el código
        # enviado al teléfono celular.
        # La api de inicio de sesion (login) debería responder con 
        # estado no válido.
        email, password = fake.email(), fake.password()
        data = {'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': email,
                'password': password}
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
        # Verificar que la api no permita autenticar usuarios.
        # Api solo puede loguear al usuario si tiene sus cuentas activas
        # Cuenta activa = ´is_active´ = True
        is_logged = self.client.login(email=email, password=password)
        self.assertFalse(is_logged)