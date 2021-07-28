from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from django.urls import reverse


class TestUserRegisterVerifyApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_with_empty_data(self):
        # Api responde con estado de error cuando se envía vacío el 
        # cuerpo de la petición. Api responde con estado de 400 BAD_REQUEST.
        user = BaseUserFactory()
        response = self.client.post(reverse('api:auth:register_verify', 
                                    kwargs={'user_id':user.id}), {})
        self.assertEqual(400, response.status_code)

    def test_api_with_user_not_souch_foud(self):
        # Api responde con estado de error cuando se envía el identificador
        # no correcto. Api responde con estado de 400 BAD_REQUEST.
        response = self.client.post(reverse('api:auth:register_verify', 
                                    kwargs={'user_id':fake.random_digit()}), {})
        self.assertEqual(400, response.status_code)
    
    def test_api_with_invalid_phone_number(self):
        # La api responde con error de estado 400 BAD_REQUEST si el 
        # teléfono contiene un formato inadecuado.
        BaseUserFactory()

        data = {'phone': fake.bothify(text='+513#########')}
        response = self.client.post(reverse('api:auth:register_verify', 
                                    kwargs={'user_id':fake.random_digit()}), data)
        self.assertEqual(400, response.status_code)
    
    def test_api_with_phone_valid_and_success(self):
        user = BaseUserFactory()

        data = {'phone': fake.bothify(text='+593#########')}
        response = self.client.post(reverse('api:auth:register_verify', 
                                    kwargs={'user_id': user.id}), data)
        self.assertEqual(201, response.status_code)
