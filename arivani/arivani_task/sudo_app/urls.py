from django.urls import path
from sudo_app.views import *
urlpatterns = [
    path('',dashboard,name="dashboard_admin"),
    path('createUserPage/',createUserPage,name="createUserPage"),
    path('registerUser/',registerUser,name="registerUser"),
    path('registerVerifyOtpPage/',registerVerifyOtpPage,name="registerVerifyOtpPage"),
    path('resendOtp/',resendOtp,name="resendOtp"),
    path('verifyOtpRegisterUser/',verifyOtpRegisterUser,name="verifyOtpRegisterUser"),
    path('employee_user_list_Page/',employee_user_list_Page,name="employee_user_list_Page"),
    path('get_user_accounts_data/',get_user_accounts_data,name="get_user_accounts_data"),
    path('change_user_status/',change_user_status,name="change_user_status"),
    path('delete_user_accounts/',delete_user_accounts,name="delete_user_accounts"),
    path('get_all_deleted_users/',get_all_deleted_users,name="get_all_deleted_users"),
    path('get_deleted_users_counts/',get_deleted_users_counts,name="get_deleted_users_counts"),
    path('restore_user/',restore_user,name="restore_user"),
    path('get_all_roles_list/',get_all_roles_list,name="get_all_roles_list"),
    path('get_role_from_front_deleted_users/',get_role_from_front_deleted_users,name="get_role_from_front_deleted_users"),
    path('get_role_from_front_users/',get_role_from_front_users,name="get_role_from_front_users"),
    path('update_user_details/',update_user_details,name="update_user_details"),
    path('hard_delete_user_accounts/',hard_delete_user_accounts,name="hard_delete_user_accounts"),
]
