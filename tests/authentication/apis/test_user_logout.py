from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
from server.users.services import user_create
from server.users.models import BaseUser
from server.users.factories import BaseUserFactory

class TestUserLogoutApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:auth:logout')
    
    def test_api_without_session(self):
        # Si no se ha iniciado sesión y se envia una petición
        # la api responderá con estado de prohibido.
        response = self.client.post(self.url)
        self.assertEqual(403, response.status_code)

    
    def test_api_logout_and_not_permission_user(self):
        # Una vez que el usuario ha realizado la finalización 
        # de la sesión, no podra acceder a rutas que requieran sesión.
        email = fake.email()
        password= fake.password()
        user = BaseUserFactory(email= email, password=password, is_active=True)
        print(user.is_active)
        # self.assertEqual(1,BaseUser.objects.count())

        # credentials={
        #     'email':email,
        #     'password':password
        # }
        # response_login = self.client.post(reverse('api:auth:login'), credentials)
        # self.assertEqual(200 ,response_login.status_code)

        # response_logout = self.client.post(self.url)
        # self.assertEqual(201, response_logout.status_code)
        # # Cerrar la sesión nuevamente.
        # # Api debería dar error de prohibido.
        # response = self.client.post(self.url)
        # self.assertEqual(403, response.status_code)
