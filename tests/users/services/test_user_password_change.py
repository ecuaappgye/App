from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.common.test_utils import fake
from server.users.services import user_password_change
from server.users.factories import BaseUserFactory
from server.users.models import BaseUser


class UserPasswordChange(TestCase):
    def setUp(self):
        self.service = user_password_change

    @ patch('server.users.services.user_password_change')
    def test_service_with_user_not_souch_found(self, user_password_change_mock):
        # Cuando el servicio recibe un identificador de usuario no
        # válido el servicio responde con error.
        password = fake.password()
        new_password = fake.password()
        BaseUserFactory(password=password)
        with self.assertRaises(ValidationError):
            self.service(user_id=fake.random_digit(),
                        old_password=password,
                        new_password=new_password,
                        password_confirm=new_password)

    @ patch('server.users.services.user_password_change')
    def test_service_passwords_not_match(self, user_password_change_mock):
        # Si el servicio recibe la contraseña acompañada de 
        # la contraseña de confirmación y estas no coinciden
        # el servicio responde con error. 
        password = fake.password()
        user = BaseUserFactory(password=password)
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id,
                        old_password=password,
                        new_password=fake.password(),
                        password_confirm=fake.password())
        
    @ patch('server.users.services.user_password_change')
    def test_service_with_old_password_invalid(self, user_password_change_mock):
        # Si el servicio recibe la contraseña anterior 
        # y ésta no es la correcta el servicio envía error.
        password = fake.password()
        new_password = fake.password()
        user = BaseUserFactory(password=password)
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            self.service(user_id=user.id,
                        old_password=fake.password(),
                        new_password=new_password,
                        password_confirm=new_password)

    @ patch('server.users.services.user_password_change')
    def test_service_with_vulnerable_password(self, user_password_change_mock):
        # Si el servicio recibe la contraseña anterior
        # válida tambien que la contraseña pase por los aspctos de seguridad. 
        password = fake.password()
        user = BaseUserFactory(password=password)
        self.assertEqual(1, BaseUser.objects.count())

        with self.assertRaises(ValidationError):
            vulnerable_password = fake.password(length=5, digits=5)
            self.service(user_id=user.id,
                        old_password=password,
                        new_password=vulnerable_password,
                        password_confirm=vulnerable_password)




