from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# class ChartsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'charts'

class ChartsConfig(AppConfig):
    name = "yeproject.test_app"
    verbose_name = _("Test_app")

    def ready(self):
        try:
            import yeproject.test_app.signals  # noqa F401
        except ImportError:
            pass