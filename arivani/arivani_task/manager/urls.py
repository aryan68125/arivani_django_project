from django.urls import path
from manager.views import *
urlpatterns = [
    path('ManagerPage/',ManagerPage,name="ManagerPage"),
    path('create_data/',create_data,name="create_data_manager"),
    path('update_data_page/<pk>/',update_data_page,name="update_data_page_manager"),
    path('update_data/',update_data,name="update_data_manager"),
    path('delete_data/<pk>',delete_data,name="delete_data_manager"),
    path('recycleBinPage/',recycleBinPage,name="recycleBinPage_manager"),
    path('restoreData_emp/<pk>',restoreData_emp,name="restoreData_emp_manager"),
    path('deleteDataPermanentlyPage/<pk>',deleteDataPermanentlyPage,name="deleteDataPermanentlyPage_manager"),
    path('deleteDataPermanently/',deleteDataPermanently,name="deleteDataPermanently_manager"),
]
