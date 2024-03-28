from django.urls import path
# from manager.views import *
# urlpatterns = [
#     path('ManagerPage/',ManagerPage,name="ManagerPage"),
#     path('create_data/',create_data,name="create_data_manager"),
#     path('update_data_page/<pk>/',update_data_page,name="update_data_page_manager"),
#     path('update_data/',update_data,name="update_data_manager"),
#     path('delete_data/<pk>',delete_data,name="delete_data_manager"),
#     path('recycleBinPage/',recycleBinPage,name="recycleBinPage_manager"),
#     path('restoreData_emp/<pk>',restoreData_emp,name="restoreData_emp_manager"),
#     path('deleteDataPermanentlyPage/<pk>',deleteDataPermanentlyPage,name="deleteDataPermanentlyPage_manager"),
#     path('deleteDataPermanently/',deleteDataPermanently,name="deleteDataPermanently_manager"),

#     path('hr_under_manager_details_page/<manager_pk>/<hr_pk>',hr_under_manager_details_page,name="hr_under_manager_details_page"),
#     path('update_hr_under_manager_details/',update_hr_under_manager_details,name="update_hr_under_manager_details"),
# ]
from manager.views2 import *
urlpatterns = [
    path('manager_dashboard/',manager_dashboard,name="manager_dashboard"),

    
    path('manager_home/',manager_home,name="manager_home"),
    path('manager_app_update_manager_profile/',manager_app_update_manager_profile,name="manager_app_update_manager_profile"),
    path('manager_add_hr_Page/',manager_add_hr_Page,name="manager_add_hr_Page"),
    path('register_hr_manager',register_hr_manager,name="register_hr_manager"),
    path('registerVerifyOtpPage_manager',registerVerifyOtpPage_manager,name="registerVerifyOtpPage_manager_app"),
    path('verifyOtpRegisterUser_manager/',verifyOtpRegisterUser_manager,name="verifyOtpRegisterUser_manager"),
    path('resendOtp_manager/',resendOtp_manager,name="resendOtp_manager_app"),
    path('manager_app_update_hr_Page/',manager_app_update_hr_Page,name="manager_app_update_hr_Page"),
    path('manager_app_update_get_all_hr/',manager_app_update_get_all_hr,name="manager_app_update_get_all_hr"),
    path('manager_app_set_hr_is_active/',manager_app_set_hr_is_active,name="manager_app_set_hr_is_active"),
    path('manager_app_gel_all_deleted_users/',manager_app_gel_all_deleted_users,name="manager_app_gel_all_deleted_users"),
    path('manager_app_restore_user/',manager_app_restore_user,name="manager_app_restore_user"),
    path('manager_app_get_all_deleted_user_count/',manager_app_get_all_deleted_user_count,name="manager_app_get_all_deleted_user_count"),
    path('manager_app_update_hr_record/',manager_app_update_hr_record,name="manager_app_update_hr_record"),
    path('manager_app_delete_user_permanently/',manager_app_delete_user_permanently,name="manager_app_delete_user_permanently"),
    path('manager_app_soft_delete_hr/',manager_app_soft_delete_hr,name="manager_app_soft_delete_hr"),

    path('manager_add_employee_Page/',manager_add_employee_Page,name="manager_add_employee_Page"),
    path('register_employee_manager/',register_employee_manager,name="register_employee_manager"),
    path('registerVerifyOtpPage_employee_manager/',registerVerifyOtpPage_employee_manager,name="registerVerifyOtpPage_employee_manager"),
    path('resendOtp_employee_manager/',resendOtp_employee_manager,name="resendOtp_employee_manager"),
    path('verifyOtpRegisterUser_employee_manager/',verifyOtpRegisterUser_employee_manager,name="verifyOtpRegisterUser_employee_manager"),
    path('manager_app_update_employee_Page/',manager_app_update_employee_Page,name="manager_app_update_employee_Page"),
    path('manager_app_update_get_all_employee/',manager_app_update_get_all_employee,name="manager_app_update_get_all_employee"),
    path('manager_app_set_employee_is_active/',manager_app_set_employee_is_active,name="manager_app_set_employee_is_active"),
    path('manager_app_soft_delete_employee/',manager_app_soft_delete_employee,name="manager_app_soft_delete_employee"),
    path('manager_app_gel_all_deleted_employee/',manager_app_gel_all_deleted_employee,name="manager_app_gel_all_deleted_employee"),
    path('manager_app_restore_employee/',manager_app_restore_employee,name="manager_app_restore_employee"),
    path('manager_app_get_all_deleted_employee_count/',manager_app_get_all_deleted_employee_count,name="manager_app_get_all_deleted_employee_count"),
    path('manager_app_update_employee_record/',manager_app_update_employee_record,name="manager_app_update_employee_record"),
    path('manager_app_delete_employee_permanently/',manager_app_delete_employee_permanently,name="manager_app_delete_employee_permanently"),

    path('manager_ass_employee_to_hr_page/',manager_ass_employee_to_hr_page,name="manager_ass_employee_to_hr_page"),
    path('get_all_employees_manager_app/',get_all_employees_manager_app,name="get_all_employees_manager_app"),
    path('get_all_hr_manager_app/',get_all_hr_manager_app,name="get_all_hr_manager_app"),
    path('assign_subordinates_manager_app/',assign_subordinates_manager_app,name="assign_subordinates_manager_app"),
    path('get_all_assigned_subordinates_manager_app/',get_all_assigned_subordinates_manager_app,name="get_all_assigned_subordinates_manager_app"),
]
