from django.db import models
from django.utils.translation import gettext as _


class User(models.Model):
    """Модель пользователя из сервиса Auth."""
    id = models.UUIDField(primary_key=True, unique=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)


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

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return self.name


class SubscriptionHistory(models.Model):
    """История подписок пользователей."""

    class Event(models.IntegerChoices):
        """События в истории."""
        ACTIVATE = 1
        DEACTIVATE = 2

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    event = models.IntegerField(choices=Event.choices)
    event_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return f'{self.user} {self.subscription}'
