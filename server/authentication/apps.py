from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "server.authentication"

    def ready(self):
        import server.authentication.signals
