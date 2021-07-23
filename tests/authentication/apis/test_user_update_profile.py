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

    def test_api_with_user_not_souch_found(self):
        response = self.client.post(reverse('api:driver:update', 
                kwargs={'user_id': fake.random_digit()}))
        self.assertEqual(403, response.status_code)
    
    def test_api_without_credentials(self):
        # La api requiere de autenticación para poder permitir el acceso
        # La api responde con estado prohibido sino encuentra permisos.
        user = BaseUserFactory()
        response = self.client.post(reverse('api:driver:update', 
                kwargs={'user_id': user.id}))
        self.assertEqual(403, response.status_code)
    
    def test_api_empty_data(self):
        # La api responde con estado de error cuando no se envía data
        # en el cuerpo de la petición.
        email = fake.email()
        password = fake.password()
        user = BaseUserFactory(email=email, password=password)
        # momento
        x= BaseUser.objects.first()
        x.is_active = True
        x.save()

        # Inicio de sesión del usuario para poder autenticar en el servidor.
        is_logged = self.client.login(email=email, password=password)
        self.assertTrue(is_logged)
        
        response = self.client.post(reverse('api:driver:update',
                        kwargs={'user_id':user.id}))
        self.assertEqual(400, response.status_code)
    
    def test_api_success(self):
        email = fake.email()
        password = fake.password()
        user = BaseUserFactory(email=email, password=password)

        # momento
        x= BaseUser.objects.first()
        x.is_active = True
        x.save()
        
        is_logged = self.client.login(email=email, password=password)
        self.assertTrue(is_logged)

        data = {'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'address': fake.address(),
                'cdi': fake.ean(length=8, prefixes=('0')),
                'phone': fake.ean(length=8, prefixes=('0'))}

        response = self.client.post(reverse('api:driver:update',
                        kwargs={'user_id':user.id}),
                        data)
        self.assertEqual(201, response.status_code)

        


    


