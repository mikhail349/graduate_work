from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode


def render_login_error(request: HttpRequest, error_msg: str) -> HttpResponse:
    """Отрендерить страницу логина с текстом ошибки.

    Args:
        request: http-запрос
        error_msg: текст ошибки

    Returns:
        HttpResponse: страница логина

    """
    context = {
        'errors': error_msg
    }
    return render(request, 'ui/login.html', context=context)


def render_error(request: HttpRequest, error_msg: str) -> HttpResponse:
    """Отрендерить страницу с ошибкой.

    Args:
        request: http-запрос
        error_msg: текст ошибки

    Returns:
        HttpResponse: страница с ошибкой

    """
    context = {
        'error': error_msg
    }
    return render(request, 'ui/error.html', context=context)


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
