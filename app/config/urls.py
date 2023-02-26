from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext as _

urlpatterns = [
    path('admin/', admin.site.urls),
]

admin.site.site_header = _('Billing service administration')
