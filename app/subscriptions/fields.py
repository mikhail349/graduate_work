from django import forms
from django.db import models
from django.utils.translation import gettext as _


class CurrencyChoices(models.TextChoices):
    """Перечисление ISO кодов валют."""
    RUB = 'rub', _('руб.')


class MoneyField(forms.DecimalField):
    """Денежное поле."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('decimal_places', 2)
        super().__init__(*args, **kwargs)


class CurrencyField(models.CharField):
    """Поле валюты."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', CurrencyChoices.choices)
        kwargs.setdefault('default', CurrencyChoices.RUB)
        super().__init__(*args, **kwargs)
