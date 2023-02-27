from services.payment.base import PaymentDetails, PaymentService


class MockPaymentService(PaymentService):
    """Мок платежного сервиса."""

    def make_payment(self, payment: PaymentDetails, payment_data: str) -> dict:
        return {
            "TransactionId": 891510444,
            "Amount": payment.amount,
            "Currency": payment.currency,
            "AccountId": payment.account_id,
            "Token": "0a0afb77-8f41-4de2-9524-1057f9695303",
            "Success": True,
        }

    def make_payment_with_token(
        self, payment: PaymentDetails, token: str
    ) -> dict:
        return {
            "TransactionId": 891510444,
            "Amount": payment.amount,
            "Currency": payment.currency,
            "AccountId": payment.account_id,
            "Token": "0a0afb77-8f41-4de2-9524-1057f9695303",
            "Success": True,
        }
