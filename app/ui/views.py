from django.shortcuts import render, redirect
from django.urls import reverse
from requests.exceptions import ConnectionError

from services.auth.auth_api_client import auth_client
from services.auth.exceptions import UnauthorizedError


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
            token = auth_client.login_user(username, password)
        except UnauthorizedError:
            context = {
                'errors': 'Неверный логин и/или пароль'
            }
            return render(request, 'ui/login.html', context=context)
        except ConnectionError:
            context = {
                'errors': 'Сервис авторизации недоступен'
            }
            return render(request, 'ui/login.html', context=context)            

        response = redirect(reverse('ui:index'))
        response.set_cookie('auth_token', token)
        return response


def logout(request):
    if request.method == 'POST':
        token = request.COOKIES.get('auth_token')
        auth_client.logout_user(token)

        response = redirect(reverse('ui:index'))
        response.delete_cookie('auth_token')
        return response
