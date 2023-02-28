from rest_framework import serializers

from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price']
