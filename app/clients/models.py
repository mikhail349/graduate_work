from django.db import models


class Client(models.Model):
    """Модель клиента.

    Fields:
        id: ИД пользователя из сервиса Auth

    """
    id = models.UUIDField(primary_key=True)

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)
