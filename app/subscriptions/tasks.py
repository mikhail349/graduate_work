import uuid

from celery import shared_task
from requests.exceptions import ConnectionError

from services.auth.auth_api_client import auth_client


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    max_retries=None
)
def add_role(user_id: uuid.UUID, role: str) -> int:
    """Отправить запрос на добавление роли в auth сервис.

    Args:
        user_id: user id
        role: название роли

    Returns:
        response status code
    """
    res = auth_client.add_user_role(user_id, role)
    return res.status_code


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    max_retries=None
)
def delete_role(user_id: uuid.UUID, role: str) -> int:
    """Отправить запрос на удаление роли в auth сервис.

    Args:
        user_id: user id
        role: название роли

    Returns:
        response status code
    """
    res = auth_client.remove_user_role(user_id, role)
    return res.status_code
