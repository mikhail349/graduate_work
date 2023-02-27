from rest_framework import serializers

from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """Представить цену с копейками."""
        return obj.price / 100

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price']