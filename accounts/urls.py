"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File:
Description:


"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name="send_login_email"),
    path('login', views.login, name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]