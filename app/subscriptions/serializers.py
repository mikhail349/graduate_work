from rest_framework import serializers

from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    paid = serializers.SerializerMethodField()

    def get_paid(self, obj):
        return obj.clientsubscription.filter(client__pk=self.context['user_id']).exists()

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price', 'duration', 'currency', 'paid']
