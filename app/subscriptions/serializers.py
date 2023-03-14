from rest_framework import serializers

from subscriptions.models import ClientSubscription, Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    duration = serializers.CharField(source='get_duration_display')
    currency = serializers.CharField(source='get_currency_display')

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price', 'duration', 'currency']


class ClientSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = ClientSubscription
        fields = ['id', 'auto_renewal', 'end_date', 'subscription']
