import functools
import uuid
from dataclasses import dataclass

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from requests.exceptions import ConnectionError

from ui import messages as msg
from ui.services.auth import auth_service
from ui.exceptions import UnauthorizedError
from ui.utils import render_error, redirect_to_login

ACCESS_TOKEN_NAME = settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME
REFRESH_TOKEN_NAME = settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME


@dataclass
class User:
    """Класс пользователя."""
    id: uuid.UUID
    email: str
    permissions: list[str]
    is_superuser: bool
    access_token: str


def has_permission(user: User, permission_name: str) -> bool:
    """Проверить, имеет ли пользователь доступ к праву.

    Args:
        user: инстанс пользователя
        permission_name: название права

    Returns:
        bool: имеет/не имеет

    """
    return user.is_superuser or permission_name in user.permissions


def get_user(access_token: str) -> User:
    """Получить пользователя из access-токена.

    Args:
        access_token: access-токен

    Returns:
        User: пользователь

    """
    payload = jwt.decode(
        access_token,
        settings.JWT_AUTH["JWT_PUBLIC_KEY"],
        algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]]
    )

    return User(
        id=payload['user_id'],
        email=payload['email'],
        permissions=payload['permissions'],
        is_superuser=payload['is_superuser'],
        access_token=access_token,
    )


def get_user_with_tokens(
    access_token: str,
    refresh_token: str
) -> tuple[User, str, str]:
    """
    Получить пользователя и токены (новые в случае истечения срока).

    Args:
        access_token: access-токен
        refresh_token: refresh-токен

    Returns:
        tuple[User, str, str]: пользователь, access-токен, refresh-токен

    """
    try:
        user = get_user(access_token)
    except jwt.ExpiredSignatureError:
        access_token, refresh_token = auth_service.refresh(refresh_token)
        user = get_user(access_token)
    return user, access_token, refresh_token


def parse_tokens(function):
    """Декоратор аутентификации пользователя из сервиса Auth через cookies.

    Проверяет access-токен на валидность.
    При истечении срока получает новые access- и refresh-токены.

    Испольузется в декораторах доступа, которые должны принять и
    вернуть пару токенов вместе с http-ответом.

    После этого, обновляет cookies полученными токенами.
    """
    @functools.wraps(function)
    def wrap(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            user, access_token, refresh_token = get_user_with_tokens(
                access_token=request.COOKIES.get(ACCESS_TOKEN_NAME),
                refresh_token=request.COOKIES.get(REFRESH_TOKEN_NAME),
            )
        except ConnectionError:
            return render_error(request, msg.AUTH_SERVICE_OFFLINE)
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            return redirect_to_login(request)
        except UnauthorizedError:
            return render_error(request, msg.UNAUTHORIZED)

        response, access_token, refresh_token = (
            function(
                request,
                user,
                access_token,
                refresh_token,
                *args,
                **kwargs,
            )
        )
        response.set_cookie(ACCESS_TOKEN_NAME, access_token)
        response.set_cookie(REFRESH_TOKEN_NAME, refresh_token)
        return response
    return wrap


def token_required(function):
    """Декоратор аутентификации пользователя из сервиса Auth через cookies."""
    @functools.wraps(function)
    @parse_tokens
    def wrap(
        request: HttpRequest,
        user: User,
        access_token: str,
        refresh_token: str,
        *args,
        **kwargs
    ) -> tuple[HttpResponse, str, str]:
        response = function(request, user, *args, **kwargs)
        return response, access_token, refresh_token
    return wrap


def token_permission_required(permission_name: str):
    """Декоратор проверки прав пользователя из сервиса Auth через cookies."""
    def inner(function):
        @functools.wraps(function)
        @parse_tokens
        def wrap(
            request: HttpRequest,
            user: User,
            access_token: str,
            refresh_token: str,
            *args,
            **kwargs
        ) -> tuple[HttpResponse, str, str]:
            if not has_permission(user, permission_name):
                try:
                    access_token, refresh_token = (
                        auth_service.refresh(refresh_token)
                    )
                    user = get_user(access_token)
                except ConnectionError:
                    return (
                        render_error(request, msg.AUTH_SERVICE_OFFLINE),
                        access_token,
                        refresh_token,
                    )
                except (
                    jwt.InvalidTokenError,
                    jwt.ExpiredSignatureError,
                    UnauthorizedError
                ):
                    return (
                        redirect_to_login(request),
                        access_token,
                        refresh_token,
                    )

                if not has_permission(user, permission_name):
                    return (
                        render_error(request, msg.UNAUTHORIZED),
                        access_token,
                        refresh_token,
                    )

            return (
                function(request, user, *args, **kwargs),
                access_token,
                refresh_token,
            )
        return wrap
    return inner
