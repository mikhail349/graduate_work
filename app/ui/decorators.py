import functools

import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode


def get_user(request):
    token = request.COOKIES.get(settings.BILLING_AUTH_TOKEN_COOKIE_NAME)

    payload = jwt.decode(
        token,
        settings.JWT_AUTH["JWT_PUBLIC_KEY"],
        algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]]
    )

    return {
        'id': payload['user_id'],
        'token': token,
        'email': payload['email'],
        'permissions': payload['permissions'],
        'is_superuser': payload['is_superuser']
    }


def redirect_to_login(request):
    return redirect(reverse('ui:login') + '?' + urlencode({'next': request.get_full_path()}))


def token_required(function):
    """Декоратор аутентификации пользователя из сервиса Auth через cookies."""
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            user = get_user(request)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return redirect_to_login(request)
        return function(request, user=user, *args, **kwargs)
    return wrap


def token_permission_required(permission_name: str):
    """Декоратор проверки прав пользователя из сервиса Auth через cookies."""
    def inner(function):
        @functools.wraps(function)
        def wrap(request, *args, **kwargs):
            try:
                user = get_user(request)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return redirect_to_login(request)

            if not user['is_superuser']:
                if permission_name not in user['permissions']:
                    return render(request, 'ui/no_access.html')

            return function(request, user=user, *args, **kwargs)
        return wrap
    return inner
