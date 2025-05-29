from django.apps import AppConfig


class MetaverseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.metaverse'
    verbose_name = '元宇宙功能'

    def ready(self):
        try:
            import apps.metaverse.signals
        except ImportError:
            pass
