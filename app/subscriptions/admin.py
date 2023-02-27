from django.contrib import admin

from subscriptions.models import Subscription, SubscriptionHistory

admin.site.register(Subscription)
admin.site.register(SubscriptionHistory)
