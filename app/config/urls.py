from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext as _

from subscriptions import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', include('subscriptions.urls')),
]
