from unittest.mock import patch

from django.contrib.sessions.models import Session
from django.test import TestCase
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.services import user_update_profile

class TestUserUniqueSession(TestCase):
    def setUp(self):
        self.service = user_update_profile
    
    @ patch('server.users.services.user_update_profile')
    def test_service(self, user_update_profile_mock):
        pass
