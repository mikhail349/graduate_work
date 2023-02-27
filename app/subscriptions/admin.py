from django.contrib import admin

from subscriptions.models import Subscription, SubscriptionHistory, User

admin.site.register(Subscription)
admin.site.register(SubscriptionHistory)
admin.site.register(User)
