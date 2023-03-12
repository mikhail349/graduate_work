from http import HTTPStatus

import requests
from django.conf import settings

from ui.exceptions import UnauthorizedError


class AuthService:
    """Класс для взаимодействия с Auth Service."""

    def __init__(self, login_url: str, logout_url: str):
        self.login_url = login_url
        self.logout_url = logout_url

    def login(self, username: str, password: str) -> str:
        """Залогинить пользователя.

        Args:
            username: имя пользователя
            password: пароль

        Returns:
            str: access-токен

        Raises:
            UnauthorizedError: неверный логин/пароль

        """

        data = {
            "username": username,
            "password": password,
        }
        res = requests.post(self.login_url, json=data)
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError()
        access_token = res.json()["access_token"]
        return access_token

    def logout(self, token: str):
        """Разлогинить пользователя.

        Args:
            token: access-токен

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        requests.post(self.logout_url, headers=headers)


auth_service = AuthService(
    login_url=f'{settings.AUTH_API}{settings.AUTH_LOGIN_ENDPOINT}',
    logout_url=f'{settings.AUTH_API}{settings.AUTH_LOGOUT_ENDPOINT}',
)
