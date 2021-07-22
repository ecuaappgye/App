from rest_framework.test import APIClient
from django.test import TestCase
from server.common.test_utils import fake
from django.urls import reverse
from server.users.services import user_create
from server.users.models import BaseUser
from server.users.factories import BaseUserFactory
from django.contrib.sessions.models import Session

class TestUserEmailChange(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_email_change_without_credentials(self):
        # La api responderá con acceso denegado cuando no reciba las
        # credenciales de sesión del usuario.
        data = {'email':fake.email()}
        response = self.client.post(reverse('api:auth:email_change', 
                                    kwargs={'user_id':fake.random_digit()}),
                                    data)
        self.assertEqual(403, response.status_code)

    def test_api_with_email_invalid(self):
        # La api recibe un formato de tipo email, si éste es incorrecto
        # deberá retornar un estado erróneo.
        email = fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)

        # momento
        x = BaseUser.objects.first()
        x.is_active = True
        x.save()

        self.client.login(email=email, password=password)
        self.assertEqual(1, Session.objects.count())
        response = self.client.post(reverse('api:auth:email_change', 
                                    kwargs={'user_id': BaseUser.objects.first().id}),
                                    {'email': fake.first_name()})
        self.assertEqual(400, response.status_code)


    def test_api_success(self):
        email = fake.email()
        password = fake.password()
        BaseUserFactory(email=email, password=password)

        # momento
        x = BaseUser.objects.first()
        x.is_active = True
        x.save()

        new_email = fake.email()
        self.client.login(email=email, password=password)
        self.assertEqual(1, Session.objects.count())
        response = self.client.post(reverse('api:auth:email_change',
                                   kwargs={'user_id': BaseUser.objects.first().id}),
                                   {'email' : new_email })
        self.assertEqual(201, response.status_code)
        # Consulta a base de datos y comparar si el email enviado 
        # esta en el registro del usuario.
        self.assertEqual(new_email, BaseUser.objects.first().email)