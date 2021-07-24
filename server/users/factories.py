import factory
from server.common.factories import ServiceFactoryMixin
from server.common.test_utils import fake
from server.users.models import BaseUser
from server.users.services import user_create


class BaseUserFactory(ServiceFactoryMixin, factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    password = fake.password()
    avatar = None
    is_active = False

    class Meta:
        model = BaseUser

    @classmethod
    def get_service(cls):
        return user_create