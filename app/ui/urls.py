from django.urls import path

from . import views

app_name = 'ui'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/',  views.profile, name='profile'),
    path('movies/', views.movies, name='movies'),
    path('movie/<int:id>/', views.movie, name='movie'),
    path('hd_movie/<int:id>/', views.hd_movie, name='hd_movie'),
    path(
        'create_checkout_session/<int:subscription_id>/',
        views.create_checkout_session,
        name='create_checkout_session'
    ),
    path('portal/', views.portal, name='portal'),
    path('success/', views.success, name='success'),
]
