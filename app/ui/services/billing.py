from http import HTTPStatus

import requests
from django.conf import settings
from requests import Response

from ui import messages as msg
from ui.exceptions import UnauthorizedError


class BillingService:
    """Класс для взаимодействия с Billing Service.

    Args:
        subscriptions_url: URL подписок
        clients_url: URL для работы с клиентами
        user_subscriptions_url: URL подписок пользователя

    """

    def __init__(
        self,
        subscriptions_url: str,
        clients_url: str,
        user_subscriptions_url: str
    ):
        self.subscriptions_url = subscriptions_url
        self.clients_url = clients_url
        self.user_subscriptions_url = user_subscriptions_url

    def create_client(self, token: str) -> Response:
        """Создать клиента.

        Args:
            token: access-токен

        Returns:
            Response: http-ответ

        Raises:
            UnauthorizedError: ошибка доступа

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.post(self.clients_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        return response

    def get_subscriptions(self, token: str) -> list:
        """Получить список активных подписок.

        Args:
            token: access-токен

        Returns:
            list: список активных подписок

        Raises:
            UnauthorizedError: ошибка доступа

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(self.subscriptions_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        return response.json()

    def get_user_subscriptions(self, token: str) -> list:
        """Получить список подписок пользователя.

        Args:
            token: access-токен

        Returns:
            list: список активных подписок

        Raises:
            UnauthorizedError: ошибка доступа

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(self.user_subscriptions_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        return response.json()


base_url = settings.BILLING_BASE_URL

billing_service = BillingService(
    subscriptions_url=f'{base_url}{settings.BILLING_SUBSCRIPTIONS_ENDPOINT}',
    clients_url=f'{base_url}{settings.BILLING_CLIENTS_ENDPOINT}',
    user_subscriptions_url=(
        f'{base_url}{settings.BILLING_USER_SUBSCRIPTIONS_ENDPOINT}'
    ),
)
