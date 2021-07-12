from django.core.exceptions import ValidationError

from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from server.api.errors import get_error_message
from importlib import import_module
from django.contrib import auth
from django.conf import settings

class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)

def get_auth_header(headers):
    value = headers.get('Authorization')

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


class SessionAsHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = get_auth_header(request.headers)

        if header is None:
            return None

        auth_type, auth_value = header

        if auth_type != 'Session':
            return None

        engine = import_module(settings.SESSION_ENGINE)
        SessionStore = engine.SessionStore
        session_key = auth_value

        request.session = SessionStore(session_key)
        user = auth.get_user(request)

        return user, None


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class ApiAuthMixin:
    authentication_classes = (
        CsrfExemptedSessionAuthentication, SessionAsHeaderAuthentication)
    permission_classes = (IsAuthenticated, )