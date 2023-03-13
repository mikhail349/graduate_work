from http import HTTPStatus

import requests
from requests import Response
from django.conf import settings

from ui import messages as msg
from ui.exceptions import UnauthorizedError


class AuthService:
    """Класс для взаимодействия с Auth Service.

    Args:
        login_url: URL логина
        logout_url: URL логаута
        refresh_url: URL обновления access-токена

    """

    def __init__(self, login_url: str, logout_url: str, refresh_url: str):
        self.login_url = login_url
        self.logout_url = logout_url
        self.refresh_url = refresh_url

    def login(self, username: str, password: str) -> tuple[str, str]:
        """Залогинить пользователя.

        Args:
            username: имя пользователя
            password: пароль

        Returns:
            tuple[str, str]: access-токен, refresh-токен

        Raises:
            UnauthorizedError: неверный логин/пароль

        """

        data = {
            "username": username,
            "password": password,
        }
        response = requests.post(self.login_url, json=data)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        
        response_json = response.json()
        return response_json["access_token"], response_json["refresh_token"]

    def logout(self, token: str) -> Response:
        """Разлогинить пользователя.

        Args:
            token: access-токен

        Returns:
            Response: http-ответ

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.post(self.logout_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        return response

    def refresh(self, token: str) -> tuple[str, str]:
        """Обновить токены на основани refresh-токена.

        Args:
            token: refresh-токен

        Returns:
            tuple[str, str]: access-токен, refresh-токен

        """
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.post(self.refresh_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            raise UnauthorizedError(msg.UNAUTHORIZED)
        response_json = response.json()
        return response_json["access_token"], response_json["refresh_token"]


auth_service = AuthService(
    login_url=f'{settings.AUTH_API}{settings.AUTH_LOGIN_ENDPOINT}',
    logout_url=f'{settings.AUTH_API}{settings.AUTH_LOGOUT_ENDPOINT}',
    refresh_url=f'{settings.AUTH_API}{settings.AUTH_REFRESH_ENDPOINT}',
)
