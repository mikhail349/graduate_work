from django.contrib import admin

from subscriptions.models import PaymentHistory, Subscription, User

admin.site.register(Subscription)
admin.site.register(PaymentHistory)
admin.site.register(User)
