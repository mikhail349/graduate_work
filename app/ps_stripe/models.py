from django.db import models
from django.utils.translation import gettext as _

from clients.models import Client
from subscriptions.models import Subscription


class Product(models.Model):
    """Модель продукта.

    Fields:
        id: ИД продукта из Stripe
        subscription: Ссылка на модель `Subscription`

    """
    id = models.CharField(_('ID'), max_length=255, primary_key=True)
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        verbose_name=_('Подписка'),
    )

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')


class Customer(models.Model):
    """Модель кастомера.

    Fields:
        id: ИД кастомера из Stripe
        сlient: Ссылка на модель `Client`

    """
    id = models.CharField(_('ID'), max_length=255, primary_key=True)
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
    )

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)

    class Meta:
        verbose_name = _('Покупатель')
        verbose_name_plural = _('Покупатели')
