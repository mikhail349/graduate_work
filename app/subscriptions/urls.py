from django.urls import path

from subscriptions import views

urlpatterns = [
    path('', views.SubscriptionsAPI.as_view()),
    path('my/', views.UserSubscriptionsAPI.as_view()),
]
