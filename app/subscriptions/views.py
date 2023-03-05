import json
import uuid
from http import HTTPStatus

import stripe
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import user_required
from subscriptions import messages as msg
from subscriptions.models import (
    PaymentHistory, Subscription, User, UserSubscription
)
from subscriptions.serializers import SubscriptionSerializer


class PaymentServiceWebhook(APIView):
    """API класс для принятия событий от платежного сервиса."""

    def post(self, request: HttpRequest):
        """Получить событие."""
        endpoint_secret = settings.STRIPE['WEBHOOK_KEY']
        payload = request.body

        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=endpoint_secret,
            )
        except stripe.error.SignatureVerificationError:
            return Response(
                data={'msg': msg.INVALID_SIGNATURE},
                status=HTTPStatus.UNAUTHORIZED,
            )

        print('event', event)
        return Response()


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
        # TODO: сконструировать запрос для воркерка/celery
        API = 'sk_test_51MhELKDyQLeD5AYiMuKMw0NLYCgKywilaVIY8ag4lHJgco0jJX6wbMWTAWNWbb8Q9DcC2YWqjI50FmqQ2jLJg4wd00pSvIAeVj'
        payload = request.body
        try:
            event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            return Response(status=400)
        print('event', event)
        # body = json.loads(request.body.decode('utf-8'))

        # user_id = body['metadata']['user_id']
        # subscription_id = body['metadata']['subscription_id']

        # subscription = Subscription.objects.get(subscription_id)
        # today = timezone.now().date()

        # with transaction.atomic():
        #     user, _ = User.objects.get_or_create(id=uuid.UUID(user_id))

        #     UserSubscription.objects.create(
        #         user=user,
        #         subscription=subscription,
        #         start_date=today,
        #         end_date=(
        #             today + relativedelta(months=subscription.months_duration)
        #         ),
        #         auto_renewal=True,
        #     )

        #     PaymentHistory.objects.create(
        #         user=user,
        #         subscription_name=subscription.name,
        #         payment_amount=body['paymentAmount'] * 100
        #     )

        return Response()

    @user_required
    def delete(self, request: HttpRequest, user_id: str):
        """Отменить подписку."""
        # TODO: сконструировать запрос для воркерка/celery

        user_subscription = UserSubscription.objects.get(user_id)
        user_subscription.auto_renewal = False
        user_subscription.save()

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
