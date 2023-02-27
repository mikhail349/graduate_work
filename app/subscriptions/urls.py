from django.urls import path

from subscriptions import views

urlpatterns = [
    path('', views.get_subscriptions),
]
