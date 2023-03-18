from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext as _

from clients.models import Client
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
        MONTHLY = 'month', _('месяц')
        YEARLY = 'year', _('год')

    name = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'))
    duration = models.CharField(
        _('Продолжительность'),
        max_length=5,
        choices=DurationChoices.choices,
        default=DurationChoices.MONTHLY,
    )
    role_name = models.CharField(
        _('Название роли'),
        max_length=255,
        help_text=_('Название роли из сервиса авторизации'),
    )
    is_active = models.BooleanField(_('Активна'), default=False)
    int_price = models.IntegerField(_('Цена'), help_text=_('Хранится в копейках'))
    currency = CurrencyField(_('Валюта'))

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

    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')


class ClientSubscription(models.Model):
    """Модель подписки клиента.

    Fields:
        client: клиент
        subscription: подписка
        start_date: дата начала действия подписки
        end_date: дата окончания действия подписки
        auto_renewal: отметка об автоматическом продлении
        payment_system_subscription_id: ИД подписки из платежной системы

    """

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name=_('Клиент'),
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name='clientsubscription',
        verbose_name=_('Подписка'),
    )
    start_date = models.DateField(_('Начало действия'))
    end_date = models.DateField(_('Окончание действия'))
    auto_renewal = models.BooleanField(_('Автопродление'), default=True)
    payment_system_subscription_id = models.CharField(
        _('ID из платежного сервиса'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Подписка клиента')
        verbose_name_plural = _('Подписки клиентов')
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'subscription'],
                name='client_subscription_client_subscription_unique'
            ),
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date')),
                name="client_subscription_start_date_le_end_date"
            ),
        ]


class PaymentHistory(models.Model):
    """История платежей пользователей.

    Fields:
        id: ИД записи
        client: клиент
        subscription_name: название подписки
        int_payment_amount: сумма платежа (в копейках)
        currency: код валюты
        payment_dt: дата и время платежа

    """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
    )
    subscription_name = models.CharField(
        _('Название подписки'),
        max_length=255,
    )
    int_payment_amount = models.IntegerField(
        _('Сумма платежа'),
        help_text=_('Хранится в копейках'),
    )
    currency = CurrencyField(_('Валюта'))
    payment_dt = models.DateTimeField(_('Дата и время платежа'))

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
        return f'{self.client} {self.subscription_name}'

    class Meta:
        verbose_name = _('История подписки')
        verbose_name_plural = _('История подписок')
