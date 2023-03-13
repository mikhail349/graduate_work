import functools
import uuid
from dataclasses import dataclass

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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


def render_auth_offline(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу с ошибкой недоступности Auth сервиса.

    Args:
        request: http-запрос

    Returns:
        HttpResponse: http-ответ

    """
    context = {
        'error': msg.AUTH_SERVICE_OFFLINE,
    }
    return render(request, 'ui/error.html', context=context)


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
    """
    Декоратор аутентификации пользователя из сервиса Auth через cookies
    и получения новых access- и refresh-токенов (при истечении срока).
    """
    @functools.wraps(function)
    def wrap(request: HttpRequest, *args, **kwargs):
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

        return function(request, user, access_token, refresh_token)
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
    ) -> HttpResponse:
        response: HttpResponse = function(request, user, *args, **kwargs)
        response.set_cookie(ACCESS_TOKEN_NAME, access_token)
        response.set_cookie(REFRESH_TOKEN_NAME, refresh_token)
        return response
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
        ) -> HttpResponse:
            if not user.is_superuser:
                if permission_name not in user.permissions:
                    try:
                        access_token, refresh_token = (
                            auth_service.refresh(refresh_token)
                        )
                        user = get_user(access_token)
                    except ConnectionError:
                        return render_error(request, msg.AUTH_SERVICE_OFFLINE)
                    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
                        return redirect_to_login(request)
                    except UnauthorizedError:
                        return render_error(request, msg.UNAUTHORIZED)

                    if not user.is_superuser:
                        if permission_name not in user.permissions:
                            return render_error(request, msg.UNAUTHORIZED)

            response: HttpResponse = function(request, user, *args, **kwargs)
            response.set_cookie(ACCESS_TOKEN_NAME, access_token)
            response.set_cookie(REFRESH_TOKEN_NAME, refresh_token)
            return response
        return wrap
    return inner