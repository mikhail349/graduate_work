from django.urls import path

from . import views

app_name = 'ui'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/',  views.profile, name='profile'),
    path('hd_movies/', views.hd_movies, name='hd_movies'),
    path(
        'create_checkout_session/<int:subscription_id>/',
        views.create_checkout_session,
        name='create_checkout_session'
    ),
    path('portal/', views.portal, name='portal')
]
