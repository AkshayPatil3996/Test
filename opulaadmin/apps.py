from django.apps import AppConfig


class OpulaadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'opulaadmin'

    def ready(self):
        import api.signals  





