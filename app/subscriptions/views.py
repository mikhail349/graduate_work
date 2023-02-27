import json

from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from auth.decorators import user_required
from subscriptions.models import Subscription, SubscriptionHistory, User
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionAPI(APIView):
    """API класс списка подписок."""

    @user_required
    def get(self, request, user):
        """Получить активные подписки."""
        active_subscriptions = (
            Subscription.objects.filter(is_active=True).all()
        )
        serializer = SubscriptionSerializer(active_subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Подключить подписку."""
        # TODO: сконструировать запрос для воркерка/celery
        body = json.loads(request.body.decode('utf-8'))

        user_id = body['metadata']['user_id']
        subscription_id = body['metadata']['subscription_id']

        user = User.objects.get(user_id)
        subscription = Subscription.objects.get(subscription_id)

        SubscriptionHistory.objects.create(
            user=user,
            subscription=subscription,
            event=SubscriptionHistory.Event.ACTIVATE,
        )

        return Response()

    @user_required
    def delete(self, request, user):
        """Отменить подписку."""
        # TODO: сконструировать запрос для воркерка/celery
        return Response()


class SubscriptionRender(APIView):
    """Класс для формирования корзины в платежной системе."""

    def post(self, request: HttpRequest):
        """Сформировать корзину в платежной системе."""
        # body = json.loads(request.body.decode('utf-8'))
        # TODO: сконструировать ответ для пс и вернуть его
        return Response()


class SubscriptionCreate(APIView):
    """Класс для оплаты подписки в платежной системе."""

    def post(self, request: HttpRequest):
        """Оплатить подписку в платежной системе."""
        # body = json.loads(request.body.decode('utf-8'))
        # todo: сконструировать ответ для пс и вернуть его
        return Response()