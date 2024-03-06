from django.urls import include, path
from auth_jwt.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('',UserRegistrationview.as_view(),name='UserRegistrationview'),
    path('VerifyEmail/',VerifyEmail.as_view(),name='VerifyEmail'),
    path('UserLoginView/',UserLoginView.as_view(),name='UserLoginView'),
    path('USerProfileView/',USerProfileView.as_view(),name='USerProfileView'),
    path('UserChangePasswordView/',UserChangePasswordView.as_view(),name='UserChangePasswordView'),
    path('SendPasswordResetEmailView/',SendPasswordResetEmailView.as_view(),name='SendPasswordResetEmailView'),
    path('reset_password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset_password'),
]