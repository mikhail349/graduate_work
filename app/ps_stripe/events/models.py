from pydantic import BaseModel


class BaseEvent(BaseModel):
    """Модель базового события."""


class Plan(BaseModel):
    """Модель плана."""
    product: str


class SubscriptonEvent(BaseEvent):
    """Модель события Подписки."""
    id: str
    customer: str
    plan: Plan
    current_period_start: int
    current_period_end: int
    cancel_at_period_end: bool


class StatusTransition(BaseModel):
    """Модель смены статуса."""
    paid_at: int


class Price(BaseModel):
    """Модель цены."""
    product: str


class InvoiceLine(BaseModel):
    """Модель позиции в счете."""
    price: Price


class InvoiceLines(BaseModel):
    """Модель корня позиций в счете."""
    data: list[InvoiceLine]


class InvoiceEvent(BaseEvent):
    """Модель события счета."""
    customer: str
    amount_paid: int
    currency: str
    status_transitions: StatusTransition
    lines: InvoiceLines


def get_subscription(data: dict) -> SubscriptonEvent:
    """Получить инстанс события подписки.

    Args:
        data: входные данные из stripe

    Returns:
        SubscriptonEvent: инстанс события подписки

    """
    return SubscriptonEvent(**data)


def get_invoice(data: dict) -> InvoiceEvent:
    """Получить инстанс события счета.

    Args:
        data: входные данные из stripe

    Returns:
        InvoiceEvent: инстанс события счета

    """
    return InvoiceEvent(**data)
