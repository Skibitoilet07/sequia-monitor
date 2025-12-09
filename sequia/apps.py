from django.apps import AppConfig

class SequiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sequia'

    def ready(self):
        # Asegura que los modelos en infrastructure/orm_models se importen
        from .infrastructure import orm_models  # noqa
