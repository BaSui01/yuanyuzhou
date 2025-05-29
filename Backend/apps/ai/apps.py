from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ai'
    verbose_name = 'AI功能'

    def ready(self):
        try:
            import apps.ai.signals
        except ImportError:
            pass
