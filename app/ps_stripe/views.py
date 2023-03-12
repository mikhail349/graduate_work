from datetime import datetime
from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework.views import APIView

from ps_stripe import messages as msg
from ps_stripe.models import Customer, Product
from subscriptions.models import ClientSubscription, PaymentHistory
from subscriptions.tasks import add_role, delete_role


def create_subscription(data):
    """Создать подписку."""
    stripe_subscription_id = data['id']
    customer = Customer.objects.get(pk=data['customer'])
    product = Product.objects.get(pk=data['plan']['product'])
    start_date = datetime.fromtimestamp(data['current_period_start'])
    end_date = datetime.fromtimestamp(data['current_period_end'])
    auto_renewal = data['cancel_at_period_end']

    ClientSubscription.objects.create(
        client=customer.client,
        subscription=product.subscription,
        start_date=start_date,
        end_date=end_date,
        auto_renewal=auto_renewal,
        payment_system_subscription_id=stripe_subscription_id,
    )

    add_role.delay(customer.client.pk, product.subscription.role_name)


def update_subscription(data):
    """Обновить подписку."""
    print(data)
    stripe_subscription_id = data['id']
    start_date = datetime.fromtimestamp(data['current_period_start'])
    end_date = datetime.fromtimestamp(data['current_period_end'])
    auto_renewal = not data['cancel_at_period_end']

    try:
        client_subscription = ClientSubscription.objects.get(
            payment_system_subscription_id=stripe_subscription_id
        )
    except ClientSubscription.DoesNotExist:
        return

    client_subscription.start_date = start_date
    client_subscription.end_date = end_date
    client_subscription.auto_renewal = auto_renewal
    client_subscription.save()


def delete_subscription(data):
    """Удалить подписку."""
    try:
        client_subscription = ClientSubscription.objects.get(
            payment_system_subscription_id=data['id']
        )
    except ClientSubscription.DoesNotExist:
        return

    client_subscription.delete()
    delete_role.delay(
        client_subscription.client.pk,
        client_subscription.subscription.role_name,
    )


def invoice_paid(data):
    """Добавить платеж в историю."""
    customer = Customer.objects.get(pk=data['customer'])
    product = Product.objects.get(
        pk=data['lines']['data'][0]['price']['product']
    )
    int_payment_amount = data['amount_paid']
    currency = data['currency']
    payment_dt = make_aware(
        datetime.fromtimestamp(data['status_transitions']['paid_at'])
    )

    PaymentHistory.objects.create(
        client=customer.client,
        subscription_name=product.subscription.name,
        int_payment_amount=int_payment_amount,
        currency=currency,
        payment_dt=payment_dt,
    )


EVENTS = {
    'customer.subscription.created': create_subscription,
    'customer.subscription.updated': update_subscription,
    'customer.subscription.deleted': delete_subscription,
    'invoice.paid': invoice_paid
}


class StripeAPI(APIView):
    """API класс для принятия событий от Stripe."""

    def post(self, request: HttpRequest):
        """Принять событие."""
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

        method = EVENTS.get(event['type'])
        if method:
            method(event['data']['object'])

        return Response()
