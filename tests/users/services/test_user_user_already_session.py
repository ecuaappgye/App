from unittest.mock import patch

from django.contrib.sessions.models import Session
from django.test import TestCase
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.services import user_already_session

class TestUserUniqueSession(TestCase):
    def setUp(self):
        self.service = user_already_session
    
    @ patch('server.users.services.user_already_session')
    def test_service_return_none_when_not_user(self, user_already_session_mock):
        # Cuando no existe una sesión que es igual o mayor que la fecha
        # de inicio de sesión del usuario retorna 'None'.
        self.assertEqual(0, Session.objects.count())

        BaseUserFactory()
        result = self.service(user=fake.random_digit())
        self.assertIsNone(result)