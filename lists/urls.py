"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.urls import path

from lists import views

urlpatterns = [
    path(r'new', views.new_list, name="new_list"),
    path(r'<list_id>/', views.view_list, name="view_list"),
    path(r'<list_id>/add_item', views.add_item, name="view_list"),
]