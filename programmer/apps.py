from django.apps import AppConfig


class ProgrammerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'programmer'

    def ready(self):
        # для работы сигналов
        import programmer.signals
