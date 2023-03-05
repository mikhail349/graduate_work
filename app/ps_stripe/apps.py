from django.apps import AppConfig


class PsStripeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ps_stripe'

    def ready(self):
        import ps_stripe.signals  # noqa: F401
