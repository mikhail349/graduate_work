from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PsStripeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ps_stripe'
    verbose_name = _('Stripe')

    def ready(self):
        import ps_stripe.signals  # noqa: F401
