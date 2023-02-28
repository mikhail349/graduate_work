from rest_framework import serializers

from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    price = serializers.SerializerMethodField()

    def get_price(self, obj) -> float:
        """Представить цену в рублях.

        Args:
            obj: объект `Subscription`

        Returns:
            float: цена в рублях

        """
        return obj.price / 100

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price']
