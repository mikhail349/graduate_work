from django.db import models
from django.utils.translation import gettext as _


class Client(models.Model):
    """Модель клиента из сервиса Auth.

    Fields:
        id: ИД пользователя
        email: эл. почта

    """
    id = models.UUIDField(_('ID'), primary_key=True)
    email = models.EmailField(_('Эл. почта'))

    def __str__(self) -> str:
        """Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.email)

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
