from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
from server.users.services import user_create
from server.users.models import BaseUser



class TestUserLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:auth:logout')
    
    def test_api_without_session(self):
        # Si no se ha iniciado sesión y se envia una petición
        # la api responderá con estado de prohibido.
        response = self.client.post(self.url)
        self.assertEqual(403, response.status_code)