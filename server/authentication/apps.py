from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = "server.authentication"
    verbose_name = "AUTENTICACIÓN"

    def ready(self):
        import server.authentication.signals
