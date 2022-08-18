"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.urls import path

from lists import views

urlpatterns = [
    path('new', views.new_list, name="new_list"),
    path('<list_id>/', views.view_list, name="view_list"),
]