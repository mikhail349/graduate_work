import datetime

from celery import shared_task
from django.conf import settings
from django.db.utils import IntegrityError
from ps_stripe.events import handler
from ps_stripe.events.models import SubscriptonEvent
from services.redis_service import redis_service

import stripe


def events_generator(event_type: str, created: int) -> stripe.Event:
    """Возвращает события заданного типа начиная с указанной даты создания.

    Args:
        event_type: тип события
        created: дата создания (timestamp)

    Returns:
        stripe.Event

    """
    objs = stripe.Event.list(
        type=event_type,
        created={"gt": created},
    )
    while objs:
        for item in objs.data:
            yield item
        objs = stripe.Event.list(
            type=event_type,
            created={"gt": created},
            starting_after=objs.data[-1],
        )


@shared_task
def create_subscriptions():
    """Создать объект подписки на основании данных, полученных из stripe."""
    start_date = int(
        (
            datetime.datetime.now()
            - datetime.timedelta(
                seconds=settings.STRIPE_EVENTS_INTERVAL,
            )
        ).timestamp()
    )
    for i in events_generator("customer.subscription.created", start_date):
        if not redis_service.exists(i["id"]):
            try:
                handler.create_subscription(
                    data=SubscriptonEvent(**i.data.object)
                )
                redis_service.put(i["id"])
            except IntegrityError:
                pass


@shared_task
def update_subscriptions():
    """Обновить объект подписки на основании данных, полученных из stripe."""
    start_date = int(
        (
            datetime.datetime.now()
            - datetime.timedelta(
                seconds=settings.STRIPE_EVENTS_INTERVAL,
            )
        ).timestamp()
    )
    for i in events_generator("customer.subscription.updated", start_date):
        if not redis_service.exists(i["id"]):
            try:
                handler.update_subscription(
                    data=SubscriptonEvent(**i.data.object)
                )
                redis_service.put(i["id"])
            except IntegrityError:
                pass


@shared_task
def delete_subscriptions():
    """Удалить объект подписки на основании данных, полученных из stripe."""
    start_date = int(
        (
            datetime.datetime.now()
            - datetime.timedelta(
                seconds=settings.STRIPE_EVENTS_INTERVAL,
            )
        ).timestamp()
    )
    for i in events_generator("customer.subscription.deleted", start_date):
        if not redis_service.exists(i["id"]):
            try:
                handler.delete_subscription(
                    data=SubscriptonEvent(**i.data.object)
                )
                redis_service.put(i["id"])
            except IntegrityError:
                pass
