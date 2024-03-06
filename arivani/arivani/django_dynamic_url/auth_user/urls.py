from django.urls import path
from auth_user.views import *
urlpatterns = [
    path('registerPage',registerPage,name="registerPage"),
    path('register',register,name="register"),
    path('registerOtpPage',registerOtpPage,name="registerOtpPage"),
    path('registerOtp',registerOtp,name="registerOtp"),
    path('loginPage',loginPage,name="loginPage"),
    path('loginUser',loginUser,name="loginUser"),
    path('logoutUser',logoutUser,name="logoutUser"),
    path('forgotPassOtpPage/<username>',forgotPassOtpPage,name="forgotPassOtpPage"),
    path('forgotPassOtpVerify',forgotPassOtpVerify,name="forgotPassOtpVerify"),
    path('changePasswordPage',changePasswordPage,name="changePasswordPage"),
    path('changePassword',changePassword,name="changePassword"),
]
