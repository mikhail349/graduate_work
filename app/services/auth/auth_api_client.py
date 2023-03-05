import os
import uuid

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../app/.env")


class AuthClient:
    """Класс для взаимодействия с сервисом auth."""

    def __init__(self):
        self.url = os.environ.get("AUTH_API")
        self.login = os.environ.get("AUTH_USERNAME")
        self.password = os.environ.get("AUTH_PASSWORD")
        self.login_endpoint = self.url + "api/v1/user/login"
        self.user_roles_endpoint = (
            self.url + "api/v1/user/{user_id}/roles/{role_name}"
        )

    def get_token(self):
        data = {
            "password": os.environ.get("AUTH_PASSWORD"),
            "username": os.environ.get("AUTH_USERNAME"),
        }
        res = requests.post(self.login_endpoint, json=data)

        access_token = res.json()["access_token"]
        return access_token

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
