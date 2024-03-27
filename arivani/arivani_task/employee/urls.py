from django.urls import path
# from employee.views import *
# urlpatterns = [
#     path("employeePage/",employeePage,name="employeePage"),
#     path("create_data/",create_data,name="create_data"),
#     path('update_data_page/<pk>',update_data_page,name="update_data_page"),
#     path('update_data/',update_data,name="update_data"),
#     path('delete_data/<pk>',delete_data,name="delete_data"),
#     path('recycleBinPage/',recycleBinPage,name="recycleBinPage_emp"),
#     path('restoreData_emp/<pk>',restoreData_emp,name="restoreData_emp"),
#     path('deleteDataPermanentlyPage/<pk>',deleteDataPermanentlyPage,name="deleteDataPermanentlyPage_emp"),
#     path('deleteDataPermanently',deleteDataPermanently,name="deleteDataPermanently")
# ]
from employee.views2 import *
urlpatterns = [
    path('employeePage/',employeePage,name="employeePage"),
    path('employee_app_update_employee_profile/',employee_app_update_employee_profile,name="employee_app_update_employee_profile"),
]
