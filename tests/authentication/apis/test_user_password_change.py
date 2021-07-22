from unittest.mock import Base
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser
from server.users.services import user_create


class TestUserPasswordChangeApi(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_api_with_user_not_souch_found(self):
        # Cuando no se envía el usuario correcto a la api
        # Debe responder con estado prohibido.
        response = self.client.post(reverse('api:auth:password_change', 
                    kwargs={'user_id':fake.random_digit()}))
        self.assertEqual(403, response.status_code)
    
    def test_api_without_credentials(self):
        # Acceso a la ruta sin credenciales
        # Api no debe permitir acceso
        BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())
        self.client.post(reverse('api:auth:password_change', 
                    kwargs={'user_id':BaseUser.objects.first().id}))
    
    def test_api_with_valid_credentials_and_success(self):
        email = fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)        
        self.assertEqual(1, BaseUser.objects.count())

        # momento...
        x = BaseUser.objects.first()
        x.is_active = True
        x.save()

        is_logged = self.client.login(email=email, password=password)
        self.assertTrue(is_logged)

        new_password = fake.password()
        data = {    
            'old_password':password,
            'new_password': new_password,
            'password_confirm':new_password
        }
        # user_id = BaseUser.objects.first().id
        # self.client.post(reverse('api:auth:password_change',
        #     kwargs={'user_id': user_id }), data)
        # self.assertEqual(201, response.status_code)

        




