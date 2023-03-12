from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import user_required
from subscriptions.models import Subscription, ClientSubscription
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionsAPI(APIView):
    """API класс списка подписок."""

    @user_required
    def get(self, request: HttpRequest, user: dict):
        """Получить действующие подписки."""
        active_subscriptions = (
            Subscription.objects.filter(is_active=True).all()
        )
        serializer = SubscriptionSerializer(active_subscriptions, many=True, context={'user_id': user['id']})
        return Response(serializer.data)
