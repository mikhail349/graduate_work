import logging
from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from ps_stripe import messages as msg
from ps_stripe.events.handler import event_registry
from services.redis_service import redis_service

logger = logging.getLogger(__name__)


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

        registered_event = event_registry.get_event(event['type'])
        if registered_event:
            try:
                registered_event.handler(
                    registered_event.transformer(event['data']['object'])
                )
            except Exception as e:
                logger.error(str(e))
                return Response(status=HTTPStatus.BAD_REQUEST)
            redis_service.put(event['id'])

        return Response()
