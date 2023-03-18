from typing import Any, Optional

import backoff
import redis
from django.conf import settings


class RedisService:
    """Класс сервиса Redis.

    Args:
        host: хост
        port: порт

    """

    def __init__(self, host: str, port: int) -> None:
        self.client = redis.Redis(host=host, port=port)

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def put(
        self,
        key: str,
        value: Optional[Any] = '',
        timeout: Optional[int] = settings.REDIS_CACHE_TIMEOUT,
    ):
        """Записать данные.

        Args:
            key: ключ
            value: значение. По умолчанию ''
            timeout: таймаут автоматического удаления.
            По умолчанию settings.REDIS_CACHE_TIMEOUT

        """
        self.client.set(key, value, ex=timeout)

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def exists(self, key: str) -> bool:
        """Проверить, существует ли ключ.

        Args:
            key: ключ

        Returns:
            bool: существует / не существует

        """
        return bool(self.client.exists(key))

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def get(self, key: str) -> Optional[Any]:
        """Получить значение ключа.

        Args:
            key: ключ

        Returns:
            Optional[Any]: значение или None

        """
        return self.client.get(key)


redis_service = RedisService(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
