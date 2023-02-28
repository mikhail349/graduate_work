from django import forms
from django.utils.translation import gettext as _

from subscriptions.models import PaymentHistory, Subscription
from utils.converters import money_to_int


class PaymentHistoryForm(forms.ModelForm):
    """Форма истории платежа."""

    int_payment_amount = forms.DecimalField(label=_('Payment amount'), max_digits=6, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['int_payment_amount'] = instance.payment_amount

    def clean_int_payment_amount(self):
        return money_to_int(self.cleaned_data['int_payment_amount'])

    class Meta:
        model = PaymentHistory
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):
    """Форма подписки."""

    int_price = forms.DecimalField(label=_('Price'), max_digits=6, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['int_price'] = instance.price

    def clean_int_price(self):
        return money_to_int(self.cleaned_data['int_price'])

    class Meta:
        model = Subscription
        fields = '__all__'
