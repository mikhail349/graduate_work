import functools
import uuid
from dataclasses import dataclass

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from ui.auth_service import auth_service
from ui.exceptions import UnauthorizedError


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


def redirect_to_login(request: HttpRequest) -> HttpResponse:
    """Перенаправить на страницу логина.

    Args:
        request: http-запрос

    Returns:
        HttpResponse: http-ответ

    """
    response = redirect(
        f'{reverse("ui:login")}?{urlencode({"next": request.get_full_path()})}'
    )
    response.delete_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
    return response


def token_required(function):
    """Декоратор аутентификации пользователя из сервиса Auth через cookies."""
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):
        new_access_token = None
        new_refresh_token = None
        try:
            user = get_user(
                request.COOKIES.get(
                    settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME,
                )
            )
        except jwt.ExpiredSignatureError:
            try:
                new_access_token, new_refresh_token = auth_service.refresh(
                    request.COOKIES.get(
                        settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME,
                    )
                )
            except UnauthorizedError:
                return redirect_to_login(request)
            user = get_user(new_access_token)
        except jwt.InvalidTokenError:
            return redirect_to_login(request)

        response = function(request, user=user, *args, **kwargs)
        if new_access_token:
            response.set_cookie(
                settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME,
                new_access_token,
            )
        if new_refresh_token:
            response.set_cookie(
                settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME,
                new_refresh_token,
            )
        return response
    return wrap


def token_permission_required(permission_name: str):
    """Декоратор проверки прав пользователя из сервиса Auth через cookies."""
    def inner(function):
        @functools.wraps(function)
        def wrap(request, *args, **kwargs):
            access_token_name = (
                settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME
            )
            refresh_token_name = (
                settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME
            )
            new_access_token = None
            new_refresh_token = None
            try:
                user = get_user(request.COOKIES.get(access_token_name))
            except jwt.ExpiredSignatureError:
                try:
                    new_access_token, new_refresh_token = auth_service.refresh(
                        request.COOKIES.get(refresh_token_name)
                    )
                except UnauthorizedError:
                    return redirect_to_login(request)
                user = get_user(new_access_token)
            except jwt.InvalidTokenError:
                return redirect_to_login(request)

            if not user.is_superuser:
                if permission_name not in user.permissions:
                    new_access_token, new_refresh_token = auth_service.refresh(
                        request.COOKIES.get(refresh_token_name) if not new_refresh_token else new_refresh_token
                    )
                    user = get_user(new_access_token)

                    if not user.is_superuser:
                        if permission_name not in user.permissions:
                            response = render(request, 'ui/no_access.html')
                            response.set_cookie(
                                access_token_name,
                                new_access_token,
                            )
                            response.set_cookie(
                                refresh_token_name,
                                new_refresh_token,
                            )
                            return response

            response = function(request, user=user, *args, **kwargs)
            if new_access_token:
                response.set_cookie(
                    access_token_name,
                    new_access_token,
                )
            if new_refresh_token:
                response.set_cookie(
                    refresh_token_name,
                    new_refresh_token,
                )
            return response

        return wrap
    return inner
