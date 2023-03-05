from django.urls import path

from ps_stripe import views

urlpatterns = [
    path('webhook/', views.StripeAPI.as_view()),
]
