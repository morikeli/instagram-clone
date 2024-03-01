from django.apps import AppConfig


class DmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dm'


    def ready(self):
        import dm.signals