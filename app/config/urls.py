from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext as _

urlapipatterns = [
    path('subscriptions/', include('subscriptions.urls')),
    path('clients/', include('clients.urls')),
    path('stripe/', include('ps_stripe.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlapipatterns)),
    path('ui/', include('ui.urls')),
]

admin.site.site_header = _('Billing service administration')
