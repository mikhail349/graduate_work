import stripe
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from clients.models import Client
from subscriptions.models import Subscription
from ps_stripe.models import Customer, Product


@receiver(post_save, sender=Subscription)
def create_update_product(
    sender,
    instance: Subscription,
    created: bool,
    **kwargs,
):
    """Создать или обновить продукт и цену в stripe."""
    if created:
        stripe_product = stripe.Product.create(
            name=instance.name,
            description=instance.description,
            active=instance.is_active
        )

        price = stripe.Price.create(
            unit_amount=instance.int_price,
            currency=instance.currency,
            recurring={"interval": instance.duration},
            product=stripe_product['id'],
        )

        stripe_product = stripe.Product.modify(
            stripe_product['id'],
            default_price=price['id'],
        )

        Product.objects.create(
            id=stripe_product['id'],
            subscription=instance
        )
    else:
        product = Product.objects.get(subscription=instance)
        stripe_product = stripe.Product.modify(
            product.pk,
            name=instance.name,
            description=instance.description,
            active=instance.is_active,
        )


@receiver(pre_delete, sender=Subscription)
def disable_product(sender, instance: Subscription, **kwargs):
    """Отключить продукт в stripe."""
    try:
        product = Product.objects.get(subscription=instance)
    except Product.DoesNotExist:
        return

    stripe.Product.modify(
        product.pk,
        active=False,
    )


@receiver(post_save, sender=Client)
def create_customer(sender, instance: Client, created: bool, **kwargs):
    """Создать клиента в stipe."""
    if created:
        stripe_customer = stripe.Customer.create(
            email=instance.email,
            metadata={"user_id": instance.pk}
        )
        Customer.objects.create(
            id=stripe_customer['id'],
            client=instance
        )


@receiver(pre_delete, sender=Client)
def delete_customer(sender, instance: Client, **kwargs):
    """Удалить клиента из stripe."""
    try:
        customer = Customer.objects.get(client=instance)
    except Customer.DoesNotExist:
        return

    stripe.Customer.delete(customer.pk)
