from django.urls import path
from auth_user.views import *
'''
OLD URLS for auth
'''
# urlpatterns=[
#     path('',registerUserPage,name="registerUserPage"),
#     path('registerUser/',registerUser,name="registerUser"),
#     path('registerVerifyOtpPage/',registerVerifyOtpPage,name="registerVerifyOtpPage"),
#     path('resendOtp/',resendOtp,name="resendOtp"),
#     path('verifyOtpRegisterUser/',verifyOtpRegisterUser,name="verifyOtpRegisterUser"),
#     path('login/',loginUserPage,name="loginUserPage"),
#     path('loginUser/',loginUser,name="loginUser"),
#     path('forgotPasswordPageUsername/',forgotPasswordPageUsername,name="forgotPasswordPageUsername"),
#     path('sendVerificationUrl/',sendVerificationUrl,name="sendVerificationUrl"),
#     path('reset_password/<uid>/<token>/',resetPassword,name="resetPassword"),
#     path('resetPasswordPage/',resetPasswordPage,name="resetPasswordPage"),
#     path('resetPassword_pass.',resetPassword_pass,name="resetPassword_pass"),
#     path('logoutUser/',logoutUser,name="logoutUser"),
#     path('ChangePasswordPage/',ChangePasswordPage,name="ChangePasswordPage"),
#     path('ChangePassword/',ChangePassword,name="ChangePassword"),
# ]

urlpatterns=[
    path('',loginUserPage,name="loginUserPage"),
    path('loginUser/',loginUser,name="loginUser"),
    path('forgotPasswordPageUsername/',forgotPasswordPageUsername,name="forgotPasswordPageUsername"),
    path('sendVerificationUrl/',sendVerificationUrl,name="sendVerificationUrl"),
    path('reset_password/<uid>/<token>/',resetPassword,name="resetPassword"),
    path('resetPasswordPage/',resetPasswordPage,name="resetPasswordPage"),
    path('resetPassword_pass.',resetPassword_pass,name="resetPassword_pass"),
    path('logoutUser/',logoutUser,name="logoutUser"),
    path('ChangePasswordPage/',ChangePasswordPage,name="ChangePasswordPage"),
    path('ChangePassword/',ChangePassword,name="ChangePassword"),
]