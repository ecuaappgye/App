from unittest.mock import Base, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_create
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserCreate(TestCase):
    def setUp(self):
        self.service = user_create

    @ patch('server.users.services.user_create')
    def test_service_with_password_vulnerable(self, user_create_mock):
        # La creación de un usuario debe pasar por una serie de
        # validadores que permitan determinar si la contraseña es
        # suficientemente robusta.
        with self.assertRaises(ValidationError):
            BaseUserFactory(password=fake.password(length=5, digits=False))

    @ patch('server.users.services.user_create')
    def test_service_with_email_already_exists(self, user_create_mock):
        # Servicio con un email ya existente.
        # El email en mayúsculas debería estar agregado en el registro.
        email = fake.email()
        BaseUserFactory(email=email)
        with self.assertRaises(ValidationError):
            BaseUserFactory(email=email.upper())

    @ patch('server.users.services.user_create')
    def test_service_with_password_none(self, user_create_mock):
        # Cuando se registra un usuario y si éste
        # envia como contraseña ´none´ o considerado como vacío.
        with self.assertRaises(ValidationError):
            BaseUserFactory(password=None)

    @ patch('server.users.services.user_create')
    def test_service_without_avatar(self, user_create_mock):
        # El registro de usuarios no tiene como obligatorio
        # el atributo avatar.
        BaseUserFactory(avatar=None)
        self.assertEqual(1, BaseUser.objects.count())

    @ patch('server.users.services.user_create')
    def test_service_and_check_account_inactive(self, user_create_mock):
        # Cuando un usuario se registra no puede permitir
        # que su atributo `is_active` sea True.
        # Para ello el servicio debe crear una cuenta desactivada.
        BaseUserFactory()
        self.assertEqual(1, BaseUser.objects.count())
        self.assertFalse(BaseUser.objects.first().is_active)
