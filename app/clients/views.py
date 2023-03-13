from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import user_required
from clients.models import Client


class ClientsAPI(APIView):
    """API класс клиентов."""

    @user_required
    def post(self, request: HttpRequest, user: dict):
        """Добавить клиента, если отсутствует."""
        Client.objects.get_or_create(id=user['id'], email=user['email'])
        return Response()
