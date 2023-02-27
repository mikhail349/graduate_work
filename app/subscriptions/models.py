from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Subscription(models.Model):
    """Модель подписки."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    role_name = models.CharField(
        max_length=255,
        help_text=_('A role name from Auth Service')
    )
    is_active = models.BooleanField(default=False)
    price = models.IntegerField(help_text=_('Stores cents'))


class SubscriptionHistory(models.Model):
    """История подписок пользователей."""

    class Event(models.IntegerChoices):
        """События в истории."""
        ACTIVATE = 1
        DEACTIVATE = 2

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    event = models.IntegerField(choices=Event.choices)
    event_dt = models.DateTimeField(auto_now_add=True)
