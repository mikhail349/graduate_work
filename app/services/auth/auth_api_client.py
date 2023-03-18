import uuid
from http import HTTPStatus
from typing import Callable

import requests
from django.conf import settings
from requests.exceptions import ConnectionError


def with_token(
    func: Callable[["AuthClient", uuid.UUID, str], requests.Response]
) -> Callable[["AuthClient", uuid.UUID, str], requests.Response]:
    """Декоратор для вызова метода и сипользованием токена.
    Если запрос с сохраненным токеном возвращает статус UNAUTHORIZED,
    запрашивается новый токен."""

    def wrapper(self: "AuthClient", *args, **kwargs) -> requests.Response:
        res = func(self, *args, **kwargs)
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            self.token = self.get_token()
            res = func(self, *args, **kwargs)
        return res

    return wrapper


class AuthClient:
    """Класс для взаимодействия с сервисом auth."""

    def __init__(self):
        self.url = settings.AUTH_API
        self.login = settings.AUTH_USERNAME
        self.password = settings.AUTH_PASSWORD
        self.login_endpoint = self.url + settings.AUTH_LOGIN_ENDPOINT
        self.user_roles_endpoint = self.url + settings.AUTH_USER_ROLE_ENDPOINT
        self.token = None

    def get_token(self) -> str | None:
        """Получить токен.

        Returns: токен

        """
        data = {
            "password": self.password,
            "username": self.login,
        }
        try:
            res = requests.post(self.login_endpoint, json=data)
        except ConnectionError:
            return None
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            return None
        access_token = res.json()["access_token"]
        return access_token

    @with_token
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
        headers = {"Authorization": "Bearer {}".format(self.token)}
        return requests.post(
            self.user_roles_endpoint.format(
                user_id=user_id, role_name=role_name
            ),
            headers=headers,
        )

    @with_token
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
        headers = {"Authorization": "Bearer {}".format(self.token)}
        return requests.delete(
            self.user_roles_endpoint.format(
                user_id=user_id, role_name=role_name
            ),
            headers=headers,
        )


auth_client = AuthClient()
