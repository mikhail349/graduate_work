from django.urls import path

from subscriptions import views

urlpatterns = [
    path('render/', views.SubscriptionRender.as_view()),
    path('create/', views.SubscriptionCreate.as_view()),
    path('webhook/', views.PaymentServiceWebhook.as_view()),
    path('', views.SubscriptionAPI.as_view()),
]
