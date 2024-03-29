from django.contrib import admin

from subscriptions.forms import PaymentHistoryForm, SubscriptionForm
from subscriptions.models import (ClientSubscription, PaymentHistory,
                                  Subscription)


class ClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'subscription',
                    'start_date', 'end_date', 'auto_renewal')


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
    list_display = ('name', 'description', 'duration',
                    'role_name', 'is_active', 'price')
    list_filter = ('is_active',)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return []
        return ['role_name', 'duration', 'int_price', 'currency']


class PaymentHistoryAdmin(admin.ModelAdmin):
    form = PaymentHistoryForm
    list_display = ('client', 'subscription_name',
                    'payment_amount', 'payment_dt')
    date_hierarchy = 'payment_dt'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(ClientSubscription, ClientSubscriptionAdmin)
