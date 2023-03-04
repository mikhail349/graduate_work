from django.db import models


class Currency(models.TextChoices):
    """Перечисление кодов валют."""
    RUB = '643'


class CurrencyField(models.CharField):
    """Поле валюты."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', Currency.choices)
        kwargs.setdefault('default', Currency.RUB)
        super().__init__(*args, **kwargs)
