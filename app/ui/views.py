import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from requests.exceptions import ConnectionError

from ui import messages as msg
from ui.auth import token_required, token_permission_required, User
from ui.exceptions import UnauthorizedError
from ui.mock import get_hd_movies
from ui.services.auth import auth_service
from ui.services.billing import billing_service
from ui.utils import render_error, render_login_error
from ps_stripe.models import Customer, Product


def index(request: HttpRequest) -> HttpResponse:
    """View домашней страницы.

    Args:
        request: http-запрос

    Returns:
        HttpResponse: домашняя страница

    """
    return render(request, 'ui/main.html')


def login(request: HttpRequest) -> HttpResponse:
    """View страницы логина.

    Args:
        request: http-запрос

    Returns:
        HttpResponse: домашняя страница

    """
    if request.method == 'GET':
        return render(request, 'ui/login.html')

    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        next = data['next']
        try:
            access_token, refresh_token = auth_service.login(
                username,
                password,
            )
        except ConnectionError:
            return render_login_error(request, msg.AUTH_SERVICE_OFFLINE)
        except UnauthorizedError:
            return render_login_error(request, msg.INVALID_CREDENTIALS)

        response = redirect(reverse('ui:index') if next == '' else next)
        response.set_cookie(
            settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME,
            access_token,
        )
        response.set_cookie(
            settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME,
            refresh_token,
        )
        return response


@token_required
def logout(request: HttpRequest, user: User) -> HttpResponse:
    """View логаута.

    Args:
        request: http-запрос
        user: пользователь

    Returns:
        HttpResponse: домашняя страница

    """
    if request.method == 'POST':
        try:
            auth_service.logout(user.access_token)
        except ConnectionError:
            return render_error(request, msg.AUTH_SERVICE_OFFLINE)
        except UnauthorizedError:
            pass

        response = redirect(reverse('ui:index'))
        response.delete_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME)
        response.delete_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
        return response


@token_required
def profile(request: HttpRequest, user: User) -> HttpResponse:
    """View страницы профиля пользователя.

    Args:
        request: http-запрос
        user: пользователь

    Returns:
        HttpResponse: страница профиля пользователя

    """
    try:
        subscriptions = billing_service.get_subscriptions(user.access_token)
        user_subscriptions = (
            billing_service.get_user_subscriptions(user.access_token)
        )
    except ConnectionError:
        return render_error(request, msg.BILLING_SERVICE_OFFLINE)
    except UnauthorizedError:
        return render_login_error(request, msg.INVALID_CREDENTIALS)

    context = {
        'subscriptions': subscriptions,
        'user_subscriptions': user_subscriptions,
        'email': user.email,
    }
    return render(request, 'ui/profile.html', context=context)


@token_required
def portal(request: HttpRequest, user: User) -> HttpResponse:
    """View портала подписок пользователя.

    Args:
        request: http-запрос
        user: пользователь

    Returns:
        HttpResponse: портал подписок пользователя

    """
    customer = Customer.objects.get(client__pk=user.id)
    session = stripe.billing_portal.Session.create(
        customer=customer.pk,
        return_url=request.build_absolute_uri(reverse('ui:profile')),
    )
    return redirect(session.url)


@token_required
def create_checkout_session(
    request: HttpRequest,
    user: User,
    subscription_id: int,
) -> HttpResponse:
    """View страницы покупки подписки.

    Args:
        request: http-запрос
        user: пользователь
        subscription_id: ИД подписки

    Returns:
        HttpResponse: страница покупки подписки

    """
    try:
        billing_service.create_client(user.access_token)
    except ConnectionError:
        return render_error(request, msg.BILLING_SERVICE_OFFLINE)
    except UnauthorizedError:
        return render_login_error(request, msg.INVALID_CREDENTIALS)

    product = Product.objects.get(subscription__id=subscription_id)
    customer = Customer.objects.get(client__pk=user.id)
    stripe_product = stripe.Product.retrieve(product.pk)
    checkout_session = stripe.checkout.Session.create(
        customer=customer.pk,
        success_url=request.build_absolute_uri(reverse('ui:profile')),
        cancel_url=request.build_absolute_uri(reverse('ui:profile')),
        mode='subscription',
        line_items=[{
            'price': stripe_product['default_price'],
            'quantity': 1
        }],
    )
    return redirect(checkout_session.url)


@token_permission_required('view_hd_movies')
def hd_movies(request: HttpRequest, user: User) -> HttpResponse:
    """View страницы с ограниченным доступом к фильмам в HD.

    Args:
        request: http-запрос
        user: пользователь

    Returns:
        HttpResponse: страница с ограниченным доступом к фильмам в HD
    """
    context = {
        'movies': get_hd_movies()
    }
    return render(request, 'ui/hd_movies.html', context=context)
