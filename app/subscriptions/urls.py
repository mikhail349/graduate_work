from django.urls import path

from subscriptions import views

urlpatterns = [
    path('', views.SubscriptionAPI.as_view()),
    path('render/', views.SubscriptionRender.as_view()),
    path('create/', views.SubscriptionCreate.as_view()),
]
