from dataclasses import dataclass
from typing import Callable

from ps_stripe.events.models import BaseEvent


@dataclass
class Event:
    """Модель события."""
    name: str
    handler: Callable[[BaseEvent], None]
    transformer: Callable[[dict], BaseEvent]


class EventRegistry:
    """Реестр событий."""

    def __init__(self) -> None:
        self.events: dict[str, Event] = {}

    def add_event(self, event: Event):
        """Добавить событие в реестр.

        Args:
            event: событие

        """
        self.events[event.name] = event

    def get_event(self, name: str) -> Event | None:
        """Получить событие из реестра по названию.

        Args:
            name: название события

        Returns:
            Event | None: событие или None

        """
        return self.events.get(name)
