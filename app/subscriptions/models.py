from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext as _

from subscriptions.fields import CurrencyField
from utils.converters import money_to_float


class Subscription(models.Model):
    """Модель подписки.

    Fields:
        id: ИД подписки
        name: название
        description: описание
        months_duration: продолжительность действия (мес.)
        role_name: название соответствюущей роли сервиса Auth
        is_active: отметка, что подписка действительна
        int_price: цена (в копейках)
        currency: код валюты

    """

    class DurationChoices(models.TextChoices):
        """Перечисление продолжительностей действия подписки."""
        MONTHLY = 'month'
        YEARLY = 'year'

    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(
        max_length=5,
        choices=DurationChoices.choices,
        default=DurationChoices.MONTHLY,
    )
    role_name = models.CharField(
        max_length=255,
        help_text=_('A role name from Auth Service')
    )
    is_active = models.BooleanField(default=False)
    int_price = models.IntegerField(help_text=_('Storing in cents'))
    currency = CurrencyField()

    @property
    def price(self) -> float:
        """Свойство - цена в рублях.

        Returns:
            float: цена в рублях

        """
        return money_to_float(self.int_price)

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return self.name


class User(models.Model):
    """Модель пользователя.

    Fields:
        id: ИД пользователя из сервиса Auth
        payment_system_customer_id: ИД пользователя в платежном сервисе

    """
    id = models.UUIDField(primary_key=True)
    payment_system_customer_id = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)


class UserSubscription(models.Model):
    """Модель подписки пользователя.

    Fields:
        user: пользователь сервиса Auth
        subscription: подписка
        start_date: дата начала действия подписки
        end_date: дата окончания действия подписки
        auto_renewal: отметка об автоматическом продлении
        payment_system_subscription_id: ИД подписки из платежной системы

    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renewal = models.BooleanField(default=True)
    payment_system_subscription_id = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscription'],
                name='user_subscription_user_subscription_unique'
            ),
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date')),
                name="user_subscription_start_date_le_end_date"
            ),
        ]


class PaymentHistory(models.Model):
    """История платежей пользователей.

    Fields:
        id: ИД записи
        user: пользователь сервиса Auth
        subscription_name: название подписки
        int_payment_amount: сумма платежа (в копейках)
        currency: код валюты
        payment_dt: дата и время платежа

    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription_name = models.CharField(max_length=255)
    int_payment_amount = models.IntegerField(help_text=_('Storing in cents'))
    currency = CurrencyField()
    payment_dt = models.DateTimeField(auto_now_add=True)

    @property
    def payment_amount(self) -> float:
        """Свойство - сумма платежа в рублях.

        Returns:
            float: сумма платежа в рублях

        """
        return money_to_float(self.int_payment_amount)

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return f'{self.user} {self.subscription_name}'

    class Meta:
        verbose_name_plural = _('Payments history')
