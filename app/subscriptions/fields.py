from django.db import models


class Currency(models.TextChoices):
    """Перечисление кодов валют."""
    RUB = '643'


class CurrencyField(models.CharField):
    """Поле валюты."""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        kwargs['choices'] = Currency.choices
        kwargs['default'] = Currency.RUB
        super().__init__(*args, **kwargs)
