from server.authentication.models import CallbackToken
from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from django.urls import reverse


class TestUserRegisterVerifyCheckApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_with_empty_data(self):
        user = BaseUserFactory()
        response = self.client.post(reverse('api:auth:register_verify_check', 
                                    kwargs={'user_id': user.id}), {})
        self.assertEqual(400, response.status_code)
    
    def test_api_with_user_not_souch_found(self):
        BaseUserFactory()
        response = self.client.post(reverse('api:auth:register_verify_check', 
                                    kwargs={'user_id': fake.random_digit()}), {})
        self.assertEqual(400, response.status_code)
    
    def test_api_with_invalid_token(self):
        user = BaseUserFactory()
        self.client.post(reverse('api:auth:register_verify',
                        kwargs={'user_id': user.id}),
                        {'phone': fake.bothify(text='+593#########')})

        self.assertEqual(1, CallbackToken.objects.count())
        response = self.client.post(reverse('api:auth:register_verify_check', 
                        kwargs={'user_id': user.id}),
                        {'token': fake.random_number(digits=6)})
        self.assertEqual(400, response.status_code)

    def test_api_with_valid_token(self):
        user = BaseUserFactory()
        self.client.post(reverse('api:auth:register_verify',
                        kwargs={'user_id': user.id}),
                        {'phone': fake.bothify(text='+593#########')})
        self.assertEqual(1, CallbackToken.objects.count())
        response = self.client.post(reverse('api:auth:register_verify_check', 
                                    kwargs={'user_id': user.id}),
                                    {'token': CallbackToken.objects.first().key})
        self.assertEqual(201, response.status_code)
