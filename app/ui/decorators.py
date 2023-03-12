import functools
from http import HTTPStatus

import jwt
from django.http import HttpResponse
from django.conf import settings

from ui import messages as msg


def token_required(function):
    """Декоратор аутентификации пользователя из сервиса Auth через cookies."""
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):
        token = request.COOKIES.get(settings.BILLING_AUTH_TOKEN_COOKIE_NAME)
        try:
            payload = jwt.decode(
                token,
                settings.JWT_AUTH["JWT_PUBLIC_KEY"],
                algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]]
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return HttpResponse(msg.UNAUTHORIZED, status=HTTPStatus.UNAUTHORIZED)
        
        data = {
            'id': payload['user_id'],
            'token': token,
            'email': payload['email'],
        }

        return function(request, user=data, *args, **kwargs)
    return wrap
