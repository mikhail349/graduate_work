import functools

import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from ui.auth_service import auth_service


def get_user(access_token):
    payload = jwt.decode(
        access_token,
        settings.JWT_AUTH["JWT_PUBLIC_KEY"],
        algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]]
    )

    return {
        'id': payload['user_id'],
        'email': payload['email'],
        'permissions': payload['permissions'],
        'is_superuser': payload['is_superuser'],
        'access_token': access_token,
    }


def redirect_to_login(request):
    response = redirect(reverse('ui:login') + '?' + urlencode({'next': request.get_full_path()}))
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
            user = get_user(request.COOKIES.get(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME))
        except jwt.ExpiredSignatureError:
            new_access_token, new_refresh_token = auth_service.refresh(
                request.COOKIES.get(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
            )
            user = get_user(new_access_token)
        except jwt.InvalidTokenError:
            return redirect_to_login(request)

        response = function(request, user=user, *args, **kwargs)
        if new_access_token:
            response.set_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME, new_access_token)
        if new_refresh_token:
            response.set_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME, new_refresh_token)
        return response
    return wrap


def token_permission_required(permission_name: str):
    """Декоратор проверки прав пользователя из сервиса Auth через cookies."""
    def inner(function):
        @functools.wraps(function)
        def wrap(request, *args, **kwargs):
            new_access_token = None
            new_refresh_token = None
            try:
                user = get_user(request.COOKIES.get(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME))
            except jwt.ExpiredSignatureError:
                new_access_token, new_refresh_token = auth_service.refresh(
                    request.COOKIES.get(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
                )
                user = get_user(new_access_token)
            except jwt.InvalidTokenError:
                return redirect_to_login(request)

            if not user['is_superuser']:
                if permission_name not in user['permissions']:
                    new_access_token, new_refresh_token = auth_service.refresh(
                        request.COOKIES.get(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
                    )
                    user = get_user(new_access_token)
                    
                    if not user['is_superuser']:
                        if permission_name not in user['permissions']:
                            response = render(request, 'ui/no_access.html')
                            response.set_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME, new_access_token)
                            response.set_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME, new_refresh_token)
                            return response

            response = function(request, user=user, *args, **kwargs)
            if new_access_token:
                response.set_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME, new_access_token)
            if new_refresh_token:
                response.set_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME, new_refresh_token)
            return response

        return wrap
    return inner
