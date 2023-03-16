from http import HTTPStatus 

from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.decorators import User, user_required
from clients.models import Client


class ClientsAPI(APIView):
    """API класс клиентов."""

    @user_required
    def post(self, request: HttpRequest, user: User) -> Response:
        """Добавить клиента, если отсутствует.

        Args:
            request: http-запрос
            user: инстанс пользователя

        Returns:
            Response: http-ответ в формате json

        """
        _, created = Client.objects.get_or_create(id=user.id,
                                                  email=user.email)
        if created:
            return Response(status=HTTPStatus.CREATED)
        return Response()
