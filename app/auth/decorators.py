import functools
from http import HTTPStatus

import jwt
from django.http import JsonResponse

from auth import messages as msg
from django.conf import settings


def response_401(msg: str) -> JsonResponse:
    """Вернуть http ответ 401 в формате json.

    Args:
        msg: текст ошибки

    Returns:
        JsonResponse: http ответ в формате json

    """
    return JsonResponse({'msg': msg}, safe=False,
                        status=HTTPStatus.UNAUTHORIZED)


def user_required(function):
    """Декоратор аутентификации пользователя из сервиса Auth."""
    @functools.wraps(function)
    def wrap(self, request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return response_401(msg.NO_CREDENTIALS)

        auth_header = request.META['HTTP_AUTHORIZATION'].split()

        if len(auth_header) != 2:
            return response_401(msg.WRONG_HEADER)

        token = auth_header[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_AUTH["JWT_PUBLIC_KEY"],
                algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]]
            )
        except jwt.ExpiredSignatureError:
            return response_401(msg.EXPIRED)

        except jwt.InvalidTokenError:
            return response_401(msg.INVALID_SIGNATURE)

        if 'user_id' not in payload or 'email' not in payload:
            return response_401(msg.INVALID_PAYLOAD)

        user = {
            'id': payload['user_id'],
            'email': payload['email'],
        }

        return function(self, request, user=user, *args, **kwargs)
    return wrap
