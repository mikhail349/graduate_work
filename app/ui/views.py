import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from requests.exceptions import ConnectionError

from ui import messages as msg
from ui.auth_service import auth_service
from ui.billing_service import billing_service
from ui.auth import token_required, token_permission_required, User
from ui.exceptions import UnauthorizedError
from ps_stripe.models import Customer, Product


def render_login_error(request, error_msg: str) -> HttpResponse:
    context = {
        'errors': error_msg
    }
    return render(request, 'ui/login.html', context=context)


def index(request):
    return render(request, 'ui/main.html')


def login(request):
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
        except UnauthorizedError:
            return render_login_error(request, msg.INVALID_CREDENTIALS)
        except ConnectionError:
            return render_login_error(request, msg.AUTH_SERVICE_OFFLINE)

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
def logout(request, user: User):
    if request.method == 'POST':
        auth_service.logout(user.access_token)

        response = redirect(reverse('ui:index'))
        response.delete_cookie(settings.BILLING_AUTH_ACCESS_TOKEN_COOKIE_NAME)
        response.delete_cookie(settings.BILLING_AUTH_REFRESH_TOKEN_COOKIE_NAME)
        return response


@token_required
def profile(request, user: User):
    subscriptions = billing_service.get_subscriptions(user.access_token)
    user_subscriptions = billing_service.get_user_subscriptions(
        user.access_token
    )
    context = {
        'subscriptions': subscriptions,
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'ui/profile.html', context=context)


@token_required
def portal(request, user: User):
    customer = Customer.objects.get(client__pk=user.id)
    session = stripe.billing_portal.Session.create(
        customer=customer.pk,
        return_url=request.build_absolute_uri(reverse('ui:profile')),
    )
    return redirect(session.url)


@token_required
def create_checkout_session(request, user: User, subscription_id: int):
    billing_service.create_client(user.access_token)
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
def hd_movies(request, user):
    return render(request, 'ui/hd_movies.html')
