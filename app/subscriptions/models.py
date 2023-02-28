from django.db import models
from django.utils.translation import gettext as _


class Subscription(models.Model):
    """Модель подписки."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    months_duration = models.IntegerField()
    role_name = models.CharField(
        max_length=255,
        help_text=_('A role name from Auth Service')
    )
    is_active = models.BooleanField(default=False)
    price = models.IntegerField(help_text=_('Storing in cents'))

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return self.name


class User(models.Model):
    """Модель пользователя из сервиса Auth."""
    id = models.UUIDField(primary_key=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)

class UserSubscription(models.Model):
    """Модель подписки пользователя."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renewal = models.BooleanField(default=True)


class PaymentHistory(models.Model):
    """История платежей пользователей."""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription_name = models.CharField(max_length=255)
    payment_amount = models.IntegerField(help_text=_('Storing in cents'))
    payment_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return f'{self.user} {self.subscription_name}'
