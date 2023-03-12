from http import HTTPStatus

import requests
from django.conf import settings

from ui.exceptions import UnauthorizedError


class BillingService:
    """Класс для взаимодействия с Billing Service."""

    def __init__(self, subscriptions_url: str, clients_url: str):
        self.subscriptions_url = subscriptions_url
        self.clients_url = clients_url
    
    def create_client(self, token: str):
        """Создать клиента.

        Args:
            token: access-токен

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        requests.post(self.clients_url, headers=headers)

    def get_subscriptions(self, token: str) -> list:
        """Получить список активных подписок.

        Args:
            token: access-токен

        Returns:
            list: список активных подписок

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(self.subscriptions_url, headers=headers)
        return response.json()

    def get_user_subscriptions(self, token: str) -> list:
        """Получить список подписок пользователя.

        Args:
            token: access-токен

        Returns:
            list: список активных подписок

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(self.subscriptions_url + 'my/', headers=headers)
        return response.json()


billing_service = BillingService(
    subscriptions_url=f'{settings.BILLING_BASE_URL}{settings.BILLING_SUBSCRIPTIONS_ENDPOINT}',
    clients_url=f'{settings.BILLING_BASE_URL}{settings.BILLING_CLIENTS_ENDPOINT}'
)
