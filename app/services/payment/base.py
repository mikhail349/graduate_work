from abc import ABC, abstractmethod

from pydantic import BaseModel


class PaymentDetails(BaseModel):
    """Класс данных платежа."""

    amount: float
    currency: str
    account_id: str


class PaymentService(ABC):
    """Абстрактный платежный сервис."""

    @abstractmethod
    def make_payment(self, payment: PaymentDetails, payment_data: str) -> dict:
        """Метод для оплаты через платежную систему.

        Args:
            payment: объект PaymentDetails с данными о платеже
            payment_data: зашифрованные данные о карте,
                          полученные со стороны клиента

        Returns:
            данные ответа платежной системы в виде словаря

        """

    @abstractmethod
    def make_payment_with_token(
        self, payment: PaymentDetails, token: str
    ) -> dict:
        """Метод для оплаты по токену.

        Args:
            payment: объект PaymentDetails с данными о платеже
            token: токен, полученный при первичной оплате

        Returns:
            данные ответа платежной системы в виде словаря
        """
