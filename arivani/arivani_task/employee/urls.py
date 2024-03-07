from django.urls import path
from employee.views import *
urlpatterns = [
    path("employeePage/",employeePage,name="employeePage"),
    path("create_data/",create_data,name="create_data"),
    path('update_data_page/<pk>',update_data_page,name="update_data_page"),
    path('update_data/',update_data,name="update_data"),
    path('delete_data/<pk>',delete_data,name="delete_data"),
]
