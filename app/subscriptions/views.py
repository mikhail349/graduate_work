from django.http import HttpRequest
from django.db.models import Exists, Q, OuterRef
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import user_required, User
from subscriptions.models import Subscription, ClientSubscription
from subscriptions.serializers import (
    ClientSubscriptionSerializer,
    SubscriptionSerializer
)


class SubscriptionsAPI(APIView):
    """API класс списка подписок."""

    @user_required
    def get(self, request: HttpRequest, user: User):
        """Получить действующие подписки, которые еще некуплены."""
        subscriptions = (
            Subscription.objects.filter(
                Q(is_active=True),
                ~Exists(ClientSubscription.objects.filter(
                    subscription__pk=OuterRef('pk'),
                    client__pk=user.id
                ))
            )
        )
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class UserSubscriptionsAPI(APIView):
    """API класс списка подписок пользователя."""

    @user_required
    def get(self, request: HttpRequest, user: User):
        """Получить подписки пользователя."""
        subscriptions = ClientSubscription.objects.filter(
            client__pk=user.id
        )
        serializer = ClientSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
