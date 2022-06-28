from django.urls import path

from authentication import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('forgot-password', views.forgot_password),
    path('reset-password/<str:hash_link>', views.reset_password),
    path('change-password', views.change_password),
]
