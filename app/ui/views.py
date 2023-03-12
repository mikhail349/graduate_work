import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from requests.exceptions import ConnectionError

from ui import messages as msg
from ui.auth_service import auth_service
from ui.billing_service import billing_service
from ui.decorators import token_required
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
        try:
            token = auth_service.login(username, password)
        except UnauthorizedError:
            return render_login_error(request, msg.INVALID_CREDENTIALS)
        except ConnectionError:
            return render_login_error(request, msg.AUTH_SERVICE_OFFLINE)           

        response = redirect(reverse('ui:index'))
        response.set_cookie(settings.BILLING_AUTH_TOKEN_COOKIE_NAME, token)
        return response


@token_required
def logout(request, user: dict):
    if request.method == 'POST':
        auth_service.logout(user['token'])

        response = redirect(reverse('ui:index'))
        response.delete_cookie(settings.BILLING_AUTH_TOKEN_COOKIE_NAME)
        return response


@token_required
def profile(request, user: dict):
    subscriptions = billing_service.get_subscriptions(user['token'])
    user_subscriptions = billing_service.get_user_subscriptions(user['token'])
    context = {
        'subscriptions': subscriptions,
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'ui/profile.html', context=context)

@token_required
def portal(request, user: dict):
    customer = Customer.objects.get(client__pk=user['id'])
    session = stripe.billing_portal.Session.create(
        customer=customer.pk,
        return_url=request.build_absolute_uri(reverse('ui:profile')),
    )
    return redirect(session.url)


@token_required
def create_checkout_session(request, user: dict, subscription_id):
    billing_service.create_client(user['token'])
    product = Product.objects.get(subscription__id=subscription_id)
    customer = Customer.objects.get(client__pk=user['id'])
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
