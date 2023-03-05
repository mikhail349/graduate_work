import uuid

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import user_required
from subscriptions.models import (
    PaymentHistory, Subscription, User, UserSubscription
)
from subscriptions.serializers import SubscriptionSerializer
from subscriptions.tasks_ import add_role, delete_role


class SubscriptionAPI(APIView):
    """API класс списка подписок."""

    @user_required
    def get(self, request: HttpRequest, user_id: str):
        """Получить действующие подписки."""
        active_subscriptions = (
            Subscription.objects.filter(is_active=True).all()
        )
        serializer = SubscriptionSerializer(active_subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        """Подключить подписку. Вызывается из ПС."""
        body = request.data

        user_id = body['metadata']['user_id']
        subscription_id = body['metadata']['subscription_id']

        subscription = Subscription.objects.get(id=subscription_id)
        today = timezone.now().date()

        with transaction.atomic():
            user, _ = User.objects.get_or_create(id=uuid.UUID(user_id))

            UserSubscription.objects.create(
                user=user,
                subscription=subscription,
                start_date=today,
                end_date=(
                    today + relativedelta(months=subscription.months_duration)
                ),
                auto_renewal=True,
            )

            PaymentHistory.objects.create(
                user=user,
                subscription_name=subscription.name,
                int_payment_amount=body['paymentAmount'] * 100
            )

        add_role.delay(user_id, subscription.role_name)

        return Response()

    @user_required
    def delete(self, request: HttpRequest, user_id: str):
        """Отменить подписку."""
        user_subscription = UserSubscription.objects.get(user__id=user_id)
        user_subscription.auto_renewal = False
        user_subscription.save()

        role = user_subscription.subscription.role_name
        delete_role.delay(user_id, role)

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
