from django.urls import path
from hr_app.views import *
from hr_app.views2 import *
# urlpatterns=[
#     path('hr_home/',dashboard_home,name="hr_home"),
#     path('insert_data/',insert_data,name="insert_data"),
#     path('get_all_data/',get_all_data,name="get_all_data"),
#     path('update_data/',update_data,name="update_data_hr"),
#     path('delete_data/',delete_data,name="delete_data"),
#     path('recycle_bin/',recycle_bin,name="recycle_bin_hr"),
#     path('recycleBinData/',recycleBinData,name='recycleBinData_hr'),
#     path('recyclebin_Data/',recyclebin_Data,name="recyclebin_Data_hr"),
#     path('restore_data_hr/',restore_data_hr,name="restore_data_hr"),
#     path('delete_data_permanently/',delete_data_permanently,name="delete_data_permanently_hr"),

#     path('employees_under_hr/',employees_under_hr,name="employees_under_hr"),
#     path('employees_under_hr_page/',employees_under_hr_page,name="employees_under_hr_page"),
#     path('employees_under_hr_list/',employees_under_hr_list,name="employees_under_hr_list"),
#     path('Update_employee_under_hr/',Update_employee_under_hr,name="Update_employee_under_hr"),
#     path('send_all_employees_under_hr_UPDATE/',send_all_employees_under_hr_UPDATE,name="send_all_employees_under_hr_UPDATE"),
#     path('send_all_employees_reset_dropdown_multiSelect/',send_all_employees_reset_dropdown_multiSelect,name="send_all_employees_reset_dropdown_multiSelect"),
# ]

urlpatterns = [
    path('hr_home/',hr_home,name="hr_home"),
    path('hr_add_employee_Page/',hr_add_employee_Page,name="hr_add_employee_Page_hr_app"),
    path('hr_app_update_employee_Page/',hr_app_update_employee_Page,name="hr_app_update_employee_Page_hr_app"),
    path('register_employee_hr/',register_employee_hr,name="register_employee_hr_app"),
    path('registerVerifyOtpPage_hr/',registerVerifyOtpPage_hr,name="registerVerifyOtpPage_hr_app"),
    path('resendOtp_hr/',resendOtp_hr,name="resendOtp_hr_app"),
    path('verifyOtpRegisterUser_hr/',verifyOtpRegisterUser_hr,name="verifyOtpRegisterUser_hr_app"),
    path('hr_app_update_get_all_employee/',hr_app_update_get_all_employee,name="hr_app_update_get_all_employee"),
]
