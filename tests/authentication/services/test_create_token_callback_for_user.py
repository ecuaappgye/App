from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.authentication.models import CallbackToken
from server.authentication.services import create_token_callback_for_user
from server.common.test_utils import fake
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserCreate(TestCase):
    def setUp(self):
        self.service = create_token_callback_for_user

    @ patch('server.authentication.services.create_token_callback_for_user')
    def test_service_user_return_callback_token(self, create_token_callback_for_user_mock):
        user : BaseUserFactory()
        data = {
            'user_id' : user.id,
            'alias_type':'mobile',
            'token_type':CallbackToken.TOKEN_TYPE_AUTH,
            'ip_address':fake.ipv4(),
            'user_agent':fake.user_agent()
        }
        self.service(data)
        self.assertEqual(1, CallbackToken.objects.count())