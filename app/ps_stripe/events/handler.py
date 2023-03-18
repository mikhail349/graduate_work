import logging
from datetime import datetime

from django.utils.timezone import make_aware

from ps_stripe import messages as msg
from ps_stripe.events.models import (BaseEvent, InvoiceEvent, SubscriptonEvent,
                                     get_invoice, get_subscription)
from ps_stripe.events.registry import Event, EventRegistry
from ps_stripe.models import Customer, Product
from subscriptions.models import ClientSubscription, PaymentHistory
from subscriptions.tasks import add_role, delete_role

logger = logging.getLogger(__name__)


def log_error(message: str, stripe_data: BaseEvent):
    """Добавить сообщение в лог.

    Args:
        message: текст сообщения
        stripe_data: входные данные из stripe

    """
    message = '{} {}'.format(
        msg.CUSTOMER_NOT_FOUND,
        stripe_data.json(),
    )
    logger.error(message)


def create_subscription(data: SubscriptonEvent):
    """Создать подписку.

    Args:
        data: данные события подписки

    """
    try:
        customer = Customer.objects.get(pk=data.customer)
    except Customer.DoesNotExist:
        log_error(msg.CUSTOMER_NOT_FOUND, data)
        raise

    try:
        product = Product.objects.get(pk=data.plan.product)
    except Product.DoesNotExist:
        log_error(msg.PRODUCT_NOT_FOUND, data)
        raise

    stripe_subscription_id = data.id
    start_date = datetime.fromtimestamp(data.current_period_start)
    end_date = datetime.fromtimestamp(data.current_period_end)
    auto_renewal = data.cancel_at_period_end

    ClientSubscription.objects.create(
        client=customer.client,
        subscription=product.subscription,
        start_date=start_date,
        end_date=end_date,
        auto_renewal=auto_renewal,
        payment_system_subscription_id=stripe_subscription_id,
    )

    add_role.delay(customer.client.pk, product.subscription.role_name)


def update_subscription(data: SubscriptonEvent):
    """Обновить подписку.

    Args:
        data: данные события подписки

    """
    stripe_subscription_id = data.id
    start_date = datetime.fromtimestamp(data.current_period_start)
    end_date = datetime.fromtimestamp(data.current_period_end)
    auto_renewal = not data.cancel_at_period_end

    try:
        client_subscription = ClientSubscription.objects.get(
            payment_system_subscription_id=stripe_subscription_id
        )
    except ClientSubscription.DoesNotExist:
        log_error(msg.CLIENT_SUBSCRIPTION_NOT_FOUND, data)
        raise

    client_subscription.start_date = start_date
    client_subscription.end_date = end_date
    client_subscription.auto_renewal = auto_renewal
    client_subscription.save()


def delete_subscription(data: SubscriptonEvent):
    """Удалить подписку.

    Args:
        data: данные события подписки

    """
    try:
        client_subscription = ClientSubscription.objects.get(
            payment_system_subscription_id=data.id
        )
    except ClientSubscription.DoesNotExist:
        log_error(msg.CLIENT_SUBSCRIPTION_NOT_FOUND, data)
        raise

    client_subscription.delete()
    delete_role.delay(
        client_subscription.client.pk,
        client_subscription.subscription.role_name,
    )


def invoice_paid(data: InvoiceEvent):
    """Добавить платеж в историю.

    Args:
        data: данные события счета

    """
    try:
        customer = Customer.objects.get(pk=data.customer)
    except Customer.DoesNotExist:
        log_error(msg.CUSTOMER_NOT_FOUND, data)
        raise

    try:
        product = Product.objects.get(
            pk=data.lines.data[0].price.product,
        )
    except Product.DoesNotExist:
        log_error(msg.PRODUCT_NOT_FOUND, data)
        raise

    int_payment_amount = data.amount_paid
    currency = data.currency
    payment_dt = make_aware(
        datetime.fromtimestamp(data.status_transitions.paid_at)
    )

    PaymentHistory.objects.create(
        client=customer.client,
        subscription_name=product.subscription.name,
        int_payment_amount=int_payment_amount,
        currency=currency,
        payment_dt=payment_dt,
    )


event_registry = EventRegistry()

event_registry.add_event(
    Event(
        name='customer.subscription.created',
        handler=create_subscription,
        transformer=get_subscription,
    )
)

event_registry.add_event(
    Event(
        name='customer.subscription.updated',
        handler=update_subscription,
        transformer=get_subscription,
    )
)

event_registry.add_event(
    Event(
        name='customer.subscription.deleted',
        handler=delete_subscription,
        transformer=get_subscription,
    )
)

event_registry.add_event(
    Event(
        name='invoice.paid',
        handler=invoice_paid,
        transformer=get_invoice,
    )
)
