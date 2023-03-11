import uuid
from http import HTTPStatus

import requests
from django.conf import settings

from services.auth.exceptions import UnauthorizedError


class AuthClient:
    """Класс для взаимодействия с сервисом auth."""

    def __init__(self):
        self.url = settings.AUTH_API
        self.login = settings.AUTH_USERNAME
        self.password = settings.AUTH_PASSWORD
        self.login_endpoint = self.url + settings.AUTH_LOGIN_ENDPOINT
        self.logout_endpoint = self.url + settings.AUTH_LOGOUT_ENDPOINT
        self.user_roles_endpoint = (
            self.url + settings.AUTH_USER_ROLE_ENDPOINT
        )

    def get_token(self):
        return self.login_user(self.login, self.password)

    def login_user(self, username, password):
        data = {
            "password": password,
            "username": username,
        }
        res = requests.post(self.login_endpoint, json=data)
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError()
        access_token = res.json()["access_token"]
        return access_token

    def logout_user(self, token):
        headers = {"Authorization": "Bearer {}".format(token)}
        return requests.post(self.logout_endpoint, headers=headers)

    def add_user_role(
        self, user_id: uuid.UUID, role_name: str
    ) -> requests.Response:
        """Добавить пользователю роль при покупке подписки.

        Args:
            user_id: user id
            role_name: название роли

        Returns:
            ответ от api сервиса auth

        """
        headers = {"Authorization": "Bearer {}".format(self.get_token())}
        return requests.post(
            self.user_roles_endpoint.format(
                user_id=user_id, role_name=role_name
            ),
            headers=headers,
        )

    def remove_user_role(
        self, user_id: uuid.UUID, role_name: str
    ) -> requests.Response:
        """Удалить роль у пользователя при окончании подписки.

        Args:
            user_id: user id
            role_name: название роли

        Returns:
            ответ от api сервиса auth

        """
        headers = {"Authorization": "Bearer {}".format(self.get_token())}
        return requests.delete(
            self.user_roles_endpoint.format(
                user_id=user_id, role_name=role_name
            ),
            headers=headers,
        )


auth_client = AuthClient()
