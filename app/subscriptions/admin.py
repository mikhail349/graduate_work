from django.contrib import admin

from subscriptions.forms import PaymentHistoryForm, SubscriptionForm
from subscriptions.models import PaymentHistory, Subscription, User, UserSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
    list_display = ('name', 'description', 'months_duration',
                    'role_name', 'is_active', 'price')
    list_filter = ('is_active',)


class PaymentHistoryAdmin(admin.ModelAdmin):
    form = PaymentHistoryForm
    list_display = ('user', 'subscription_name',
                    'payment_amount', 'payment_dt')
    date_hierarchy = 'payment_dt'

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class UserAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription)