from django.urls import path
from hr_app.views import *
urlpatterns=[
    path('hr_home/',dashboard_home,name="hr_home"),
    path('insert_data/',insert_data,name="insert_data"),
    path('get_all_data/',get_all_data,name="get_all_data"),
    path('update_data/',update_data,name="update_data_hr"),
    path('delete_data/',delete_data,name="delete_data"),
    path('recycle_bin/',recycle_bin,name="recycle_bin_hr"),
    path('recycleBinData/',recycleBinData,name='recycleBinData_hr'),
    path('recyclebin_Data/',recyclebin_Data,name="recyclebin_Data_hr"),
    path('restore_data_hr/',restore_data_hr,name="restore_data_hr"),
    path('delete_data_permanently/',delete_data_permanently,name="delete_data_permanently_hr"),

    path('employees_under_hr/',employees_under_hr,name="employees_under_hr"),
    path('employees_under_hr_page/',employees_under_hr_page,name="employees_under_hr_page"),
    path('employees_under_hr_list/',employees_under_hr_list,name="employees_under_hr_list"),
    path('Update_employee_under_hr/',Update_employee_under_hr,name="Update_employee_under_hr"),
]