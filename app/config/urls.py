from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', include('subscriptions.urls')),
]

admin.site.site_header = _('Billing service administration')
