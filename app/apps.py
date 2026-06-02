from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        from .django_compat import patch_template_context_copy

        patch_template_context_copy()
