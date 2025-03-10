from django.apps import AppConfig


class DestinationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'destination_app'

    def ready(self):
        import destination_app.signals


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.signals  