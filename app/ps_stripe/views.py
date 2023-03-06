from datetime import datetime
from http import HTTPStatus

import stripe
from django.db import transaction
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from ps_stripe import messages as msg
from ps_stripe.models import Customer, Product
from subscriptions.models import ClientSubscription, PaymentHistory
from subscriptions.tasks import add_role, delete_role


def create_subscription(data):
    stripe_subscription_id = data['id']
    client = Customer.objects.get(pk=data['customer']).client
    subscription = Product.objects.get(pk=data['plan']['product']).subscription
    start_date = datetime.fromtimestamp(data['current_period_start'])
    end_date = datetime.fromtimestamp(data['current_period_end'])
    auto_renewal = True
    int_payment_amount = data['plan']['amount']
    currency = data['plan']['currency']
    payment_dt = datetime.fromtimestamp(data['plan']['created'])

    with transaction.atomic():
        ClientSubscription.objects.create(
            client=client,
            subscription=subscription,
            start_date=start_date,
            end_date=end_date,
            auto_renewal=auto_renewal,
            payment_system_subscription_id=stripe_subscription_id,
        )

        PaymentHistory.objects.create(
            client=client,
            subscription_name=subscription.name,
            int_payment_amount=int_payment_amount,
            currency=currency,
            payment_dt=payment_dt,
        )

    add_role(client.pk, subscription.role_name)


def delete_subscription(data):
    client_subscription = ClientSubscription.objects.get(
        payment_system_subscription_id=data['id']
    )
    client_subscription.delete()
    delete_role(
        client_subscription.client.pk,
        client_subscription.subscription.role_name,
    )


EVENTS = {
    'customer.subscription.created': create_subscription,
    'customer.subscription.deleted': delete_subscription,
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
