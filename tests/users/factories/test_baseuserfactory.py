from unittest.mock import patch

from django.test import TestCase
from server.users.factories import BaseUserFactory


class BaseUserFactoryTests(TestCase):
    @patch('server.users.factories.user_create')
    def test_creating_with_factory_call_service(self, user_create_mock):
        BaseUserFactory()
        self.assertTrue(user_create_mock.called)
        self.assertEqual(1, user_create_mock.call_count)


