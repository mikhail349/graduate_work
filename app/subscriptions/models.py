from django.db import models
from django.utils.translation import gettext as _


class Subscription(models.Model):
    """Модель подписки.

    Fields:
        id: ИД подписки
        name: название
        description: описание
        months_duration: продолжительность действия (мес.)
        role_name: название соответствюущей роли из сервиса Auth
        is_active: отметка, что подписка действительна
        price: цена (в копейках)

    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    months_duration = models.IntegerField()
    role_name = models.CharField(
        max_length=255,
        help_text=_('A role name from Auth Service')
    )
    is_active = models.BooleanField(default=False)
    price = models.IntegerField(help_text=_('Storing in cents'))

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return self.name


class User(models.Model):
    """Модель пользователя из сервиса Auth.

    Fields:
        id: ИД пользователя

    """
    id = models.UUIDField(primary_key=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return str(self.id)


class UserSubscription(models.Model):
    """Модель подписки пользователя.

    Fields:
        user: пользователь из сервиса Auth
        subscription: подписка
        start_date: дата начала действия подписки
        end_date: дата окончания действия подписки
        auto_renewal: отметка об автоматическом продлении

    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renewal = models.BooleanField(default=True)


class PaymentHistory(models.Model):
    """История платежей пользователей.

    Fields:
        id: ИД записи
        user: пользователь из сервиса Auth
        subscription_name: название подписки
        payment_amount: сумма платежа (в копейках)
        payment_dt: дата и время платежа

    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription_name = models.CharField(max_length=255)
    payment_amount = models.IntegerField(help_text=_('Storing in cents'))
    payment_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Магический метод текстового представления модели.

        Returns:
            str: текстовое представление модели

        """
        return f'{self.user} {self.subscription_name}'
