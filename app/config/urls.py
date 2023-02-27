from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext as _

urlapipatterns = [
    path('subscriptions/', include('subscriptions.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlapipatterns)),
]

admin.site.site_header = _('Billing service administration')
