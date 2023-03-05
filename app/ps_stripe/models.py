from django.db import models

from clients.models import Client
from subscriptions.models import Subscription


class Product(models.Model):
    """Модель продукта.

    Fields:
        id: ИД продукта из Stripe
        subscription: Ссылка на модель `Subscription`

    """
    id = models.CharField(max_length=255, primary_key=True)
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
    )


class Customer(models.Model):
    """Модель кастомера.

    Fields:
        id: ИД кастомера из Stripe
        сlient: Ссылка на модель `Client`
        
    """
    id = models.CharField(max_length=255, primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)
