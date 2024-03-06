from django.urls import path
from dashboard.views import *
urlpatterns=[
    path('',dashboard_home,name="dashboard_home"),
    path('insert_data/',insert_data,name="insert_data"),
    path('get_all_data/',get_all_data,name="get_all_data"),
    path('update_data/',update_data,name="update_data"),
    path('delete_data/',delete_data,name="delete_data"),
]