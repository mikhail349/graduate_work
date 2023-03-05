from django.db import models

from subscriptions.models import Subscription

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
    )
